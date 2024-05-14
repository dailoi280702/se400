from flask import Flask, request, jsonify
import torch
from model import CourseRecommendationModel  # Replace with your model definition
import pandas as pd
import sys
import signal
import threading

# from sklearn.model_selection import train_test_split


app = Flask(__name__)
ROUTE_PREFIX = "/recommendation-model"

# Load your pre-trained model (optional)
model = CourseRecommendationModel.load_from_file("model.pt")  # Replace with your path


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
        data = request.get_json()
        user_history_ids = data.get("course_ids", [])

        if not user_history_ids:
            return jsonify({"error": "Missing course IDs in request body"}), 400

        # Preprocess user history IDs (optional)
        # ... (e.g., convert to numerical representations)

        # Predict recommendations using the model
        recommended_courses = model.predict(user_history_ids)

        # Return recommended course IDs
        return jsonify({"recommended_courses": recommended_courses})

    except Exception as e:
        print(f"An error occurred during prediction: {e}")
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
        if not model.isTraining:
            thread = threading.Thread(target=lambda: model.train())
            thread.run

        # Save the trained model
        model.save_to_file("model.pt")  # Replace with your path

        return jsonify({"message": "Model retraining triggered!"})

    except Exception as e:
        print(f"An error occurred during retraining: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    signal.signal(
        signal.SIGTERM,
        lambda sig, frame: sys.exit(0),
    )

    app.run(host="0.0.0.0", port=5000)  # Run the API on port 5000
