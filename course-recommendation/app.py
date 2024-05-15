from collections import defaultdict
from flask import Flask, request, jsonify
from torch import nn
from torch.utils.data import Dataset, DataLoader
from threading import Thread
import csv
import signal
import sys
import time
import torch
import torch
import traceback
import os


class SimilarItemsDataset(Dataset):
    def __init__(self, data_path):
        self.data = []
        self.id2idx = {}
        self.tag_dict = defaultdict(int)
        self.read_data(data_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item_id, tags, rating = self.data[idx]
        tag_idxs = [self.tag_dict[tag] for tag in tags.split()]
        return torch.tensor(item_id), torch.tensor(tag_idxs), torch.tensor(rating)

    def read_data(self, data_path):
        with open(data_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for idx, row in enumerate(reader):
                item_id, tags, rating = row[0], row[2], row[1]
                self.data.append((int(item_id), tags, float(rating)))
                self.id2idx[int(item_id)] = idx
                for tag in tags.split():
                    self.tag_dict[tag] += 1

        # Assign unique integer values to tags
        self.tag_to_indx = {tag: idx for idx, tag in enumerate(self.tag_dict)}


class SimilarItemsModel(torch.nn.Module):
    def __init__(self, num_tags, embedding_dim):
        super(SimilarItemsModel, self).__init__()
        self.embedding = torch.nn.Embedding(num_tags, embedding_dim)
        self.fc1 = torch.nn.Linear(embedding_dim, 64)
        self.fc2 = torch.nn.Linear(64, 1)

    def forward(self, tag_idxs):
        embeddings = self.embedding(tag_idxs)
        # Average embedding vectors for all tags in an item
        avg_embedding = torch.mean(embeddings, dim=1)
        hidden = torch.nn.functional.relu(self.fc1(avg_embedding))
        return torch.sigmoid(self.fc2(hidden))


def train(model, train_loader, optimizer, criterion, num_epochs, save_model_path=None):
    print("Start training model", flush=True)
    min_rating = float("inf")  # Initialize min_rating outside the loop
    max_rating = float("-inf")  # Initialize max_rating outside the loop

    start_time = time.time()  # Start training time measurement

    for item_id, tag_idxs, rating in train_loader:
        batch_min_rating = float("inf")
        batch_max_rating = float("-inf")

        min_rating = min(min_rating, batch_min_rating)  # Update overall min
        max_rating = max(max_rating, batch_max_rating)  # Update overall max

    for epoch in range(num_epochs):
        for item_id, tag_idxs, rating in train_loader:
            optimizer.zero_grad()

            outputs = model(tag_idxs)
            loss = nn.functional.mse_loss(outputs, rating.unsqueeze(1))  # Use MSE

            loss.backward()
            optimizer.step()
        # print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

    end_time = time.time()  # End training time measurement
    training_time = end_time - start_time
    print(f"Model training completed, time: {training_time:.2f} seconds", flush=True)

    if save_model_path:  # Save model if path is provided
        torch.save(model.state_dict(), save_model_path)


def is_rating_continuous(rating):
    # Assuming rating is a tensor
    return rating.min().item() >= 0 and rating.max().item() <= 5  # Check for 0-5 range


def predict(model, item_ids, dataset, k=10):
    """
    Recommends similar items for a list of item IDs.

    Args:
        model: The trained SimilarItemsModel.
        item_ids: A list of item IDs for which recommendations are needed.
        dataset: The SimilarItemsDataset containing item data.
        k: The number of top similar items to recommend (default: 10).

    Returns:
        A single flattened list containing all unique recommended item IDs for the
        provided list of item IDs (excluding duplicates and original items).
    """

    all_recommendations = []
    for item_id in item_ids:
        # Get item embedding (same logic as before)
        item_idx = dataset.id2idx[item_id]
        item_tags = dataset.data[item_idx][1]
        tag_idxs = torch.tensor([dataset.tag_to_indx[tag] for tag in item_tags.split()])
        item_embedding = torch.mean(model.embedding(tag_idxs), dim=0)

        # Calculate similarity with all items
        similarities = torch.zeros(len(dataset))
        for idx, (data_id, data_tag_idxs, _) in enumerate(dataset):
            data_embedding = torch.mean(model.embedding(data_tag_idxs), dim=0)
            similarities[idx] = torch.dot(item_embedding, data_embedding)

        # Sort by similarity and select top k similar items (excluding the original item)
        top_k_idxs = torch.topk(similarities, k, dim=0)[1].squeeze()
        recommendations = [dataset.data[i][0] for i in top_k_idxs if i != item_idx]

        # Add recommendations for this item to the all_recommendations list
        all_recommendations.extend(recommendations)

    # Remove duplicate recommendations and original item IDs
    unique_recommendations = list(
        set(all_recommendations)
    )  # Convert to set for deduplication
    unique_recommendations = [
        item for item in unique_recommendations if item not in item_ids
    ]

    return unique_recommendations


# Define custom collate function for padding
def pad_collate(batch):
    # Get a list of lengths of each list of tags in the batch
    lengths = [len(x[1]) for x in batch]
    # Find the maximum length
    max_len = max(lengths)

    # Pad shorter lists with zeros to reach the maximum length
    padded_tags = []
    # Pad shorter lists with zeros to reach the maximum length
    padded_tags = []
    for item_id, tags, rating in batch:
        padded_tags.append(
            (item_id, torch.nn.functional.pad(tags, (0, max_len - len(tags))), rating)
        )

    # Convert padded lists to tensors
    item_ids, tag_idxs, ratings = zip(*padded_tags)
    item_ids = torch.stack(item_ids)
    tag_idxs = torch.stack(tag_idxs)
    ratings = torch.stack(ratings)

    return item_ids, tag_idxs, ratings


def load_model(model_path):
    global num_tags, embedding_dim
    model = SimilarItemsModel(num_tags, embedding_dim)  # Create model instance
    model.load_state_dict(torch.load(model_path))  # Load model parameters
    model.eval()  # Set model to evaluation mode for prediction
    return model


# API layer

app = Flask(__name__)
ROUTE_PREFIX = "/recommendation-model"

global model, dataset
training_in_progress = False
model = None

# Load model on startup (optional, adjust path as needed)
model_path = "/data/saved_model.pt"
data_path = "/data/processed_data.csv"
if os.path.exists(model_path):
    global num_tags, embedding_dim
    dataset = SimilarItemsDataset(data_path)
    num_tags = len(dataset.tag_dict)
    embedding_dim = 32
    model = load_model(model_path)
    print("Model loaded successfully!")
else:
    print("Model not found. Please train the model before using the API.")


@app.errorhandler(Exception)  # Catch all exceptions
def handle_error(error):
    """Handles all application errors and returns a JSON response with the error message.

    Args:
        error (Exception): The exception that occurred.

    Returns:
        flask.wrappers.Response: A JSON response with the error message and appropriate status code.
    """

    # Get the HTTP status code from the error (if available)
    status_code = getattr(error, "code", 500)  # Default to 500 for unhandled exceptions

    # Create a JSON response with the error message
    response = jsonify({"message": str(error)})
    response.status_code = status_code

    # Log the error for debugging purposes
    app.logger.error(f"An error occurred: {error}")

    return response


@app.route(f"{ROUTE_PREFIX}/predict", methods=["POST"])
def predict_courses():
    """
    Predicts recommended courses based on user history (course IDs).

    Returns:
        JSON: {"recommended_courses": [list of course IDs]} on success.
             JSON: {"error": "Error message"} on error.
    """

    try:
        # Get user history course IDs from request body
        predictions = []
        if model:
            data = request.get_json()
            user_history_ids = data.get("course_ids", [])

            if not user_history_ids:
                return jsonify({"error": "Missing course IDs in request body"}), 400

            if not model or not dataset:
                return jsonify({"error": "Model or dataset not loaded"}), 500

            # Make prediction using the model and dataset
            predictions = predict(model, user_history_ids, dataset)

        return jsonify({"recommended_courses": predictions})

    except Exception as e:
        print(f"An error occurred during prediction: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route(f"{ROUTE_PREFIX}/retrain", methods=["POST"])
def retrain_model():
    """
    Retrains the model based on updated data (triggered by a webhook).

    Returns:
        JSON: {"message": "Model retraining triggered!"} on success.
             JSON: {"error": "Error message"} on error.
    """

    try:
        # Trigger model retraining in a separate thread for non-blocking behavior
        global training_in_progress
        if not training_in_progress:
            retrain_thread = Thread(target=retrain_in_thread)
            retrain_thread.start()
        else:
            return jsonify(
                {"message": "Model is still training, please call retrain event later!"}
            )

        return jsonify({"message": "Model retraining triggered!"})

    except Exception as e:
        print(f"An error occurred during retraining: {e}", flush=True)
        return jsonify({"error": "Internal server error"}), 500


def retrain_in_thread():
    """
    Retrains the model in a separate thread.
    """

    try:
        global model, dataset, num_tags, embedding_dim
        dataset = SimilarItemsDataset(data_path)
        num_tags = len(dataset.tag_dict)
        embedding_dim = 32
        batch_size = 32
        learning_rate = 0.001

        model = SimilarItemsModel(num_tags, embedding_dim)
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        # Create data loaders with custom collate function
        train_loader = DataLoader(
            dataset, batch_size=batch_size, shuffle=True, collate_fn=pad_collate
        )
        # val_loader (optional) = DataLoader(...)

        # Train the model
        num_epochs = 10
        train(model, train_loader, optimizer, criterion, num_epochs, model_path)

        print("Model retraining completed!")

    except Exception as e:
        print(f"An error occurred during retraining: {e}", flush=True)


if __name__ == "__main__":
    # load model if file exist

    signal.signal(
        signal.SIGTERM,
        lambda sig, frame: sys.exit(0),
    )

    app.run(host="0.0.0.0", port=5000)  # Run the API on port 5000
