from flask import Flask, request, jsonify
from threading import Thread
import signal
import sys
import time
import torch
import torch
import traceback
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import math

global similarity, data
data_path = "/data/processed_data.csv"
model_path = "/data/saved_model.pkl"


def train(data_path, save_path=None):
    print("Start training model", flush=True)
    start_time = time.time()  # Start training time measurement

    global data, similarity
    data = pd.read_csv(data_path)
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(data["tags"]).toarray()
    ps = PorterStemmer()

    def stem(text):
        y = []

        for i in text.split():
            y.append(ps.stem(i))

        return " ".join(y)

    data["tags"] = data["tags"].apply(stem)  # applying stemming on the tags column
    similarity = cosine_similarity(vectors)

    end_time = time.time()  # End training time measurement
    training_time = end_time - start_time
    print(f"Model training completed, time: {training_time:.2f} seconds", flush=True)

    if save_path:
        try:
            with open(save_path, "wb") as f:
                pickle.dump(similarity, f)
        except PermissionError as e:
            print(f"Error saving similarity matrix: {e}", flush=True)


def recommend_ids(list_of_ids, n=10):
    global similarity, data

    # Handle empty list case
    if not list_of_ids:
        return []

    course_recommendations = []
    for id in list_of_ids:
        course_recommendations.extend(recommend(id, math.ceil(n / len(list_of_ids))))

    return list(set(course_recommendations))


def recommend(id, n=2):
    if n < 2:
        n = 2

    global data, similarity
    try:
        course_index = data[data["id"] == id].index[0]
        distances = similarity[course_index]
        course_list = sorted(
            list(enumerate(distances)), reverse=True, key=lambda x: x[1]
        )[1 : n + 1]

        res = []
        for i in course_list:
            res.append(int(data.iloc[i[0]].id))
        return res
    except IndexError:
        return []


def load_model(model_path):
    global similarity, data
    data = pd.read_csv(data_path)
    with open(model_path, "rb") as f:
        similarity = pickle.load(f)


# API layer

app = Flask(__name__)
ROUTE_PREFIX = "/recommendation-model"

training_in_progress = False

# Load model on startup (optional, adjust path as needed)
if os.path.exists(model_path):
    load_model(model_path)
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
        predictions = []
        if similarity.any():
            data = request.get_json()
            user_history_ids = data.get("course_ids", [])

            if not user_history_ids:
                return jsonify({"error": "Missing course IDs in request body"}), 400

            predictions = recommend_ids(user_history_ids, 20)

            print(predictions, flush=True)

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
            training_in_progress = True
            retrain_thread = Thread(target=retrain_in_thread)
            retrain_thread.start()
            training_in_progress = False
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
        train(data_path, model_path)

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
