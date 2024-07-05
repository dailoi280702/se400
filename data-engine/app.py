import requests  # Import requests library for making HTTP requests
from flask import Flask, request, jsonify
from warehouse import process_data_from_db
import signal
import sys
from decouple import config
import sentry_sdk
import os


app = Flask(__name__)
ROUTE_PREFIX = "/warehouse"

DEFAULT_WEBHOOK_URL = "http://course-recommendation:5000/recommendation-model/retrain"


@app.route(f"{ROUTE_PREFIX}/process_data", methods=["POST"])
def process_data():
    """
    Triggers data processing logic on demand and sends a webhook notification.

    Returns:
        JSON: {"message": "Data processing successful!"} on success.
              JSON: {"error": "Error message"} on error.
    """

    try:
        webhook_url = ""
        try:
            data = request.get_json()
            webhook_url = data.get("webhook_url", "")
        except:
            pass

        if webhook_url == "":
            webhook_url = config("TRAIN_MODEL_WEBHOOK_URL")

        process_data_from_db()

        if not webhook_url:
            webhook_url = DEFAULT_WEBHOOK_URL

        try:
            response = requests.post(
                webhook_url,
                json={},
                auth=("airflow", "airflow"),
            )
            response.raise_for_status()  # Raise exception for non-2xx status codes
            print(
                f"Webhook sent to {webhook_url} (status code: {response.status_code})"
            )
        except requests.exceptions.RequestException as e:
            print(f"Error sending webhook to {webhook_url}: {e}")

        try:
            sentry_sdk.capture_message("Data processing successful")
        except:
            pass
        # Return success message
        return jsonify({"message": "Data processing successful!"})

    except Exception as e:  # Catch any unexpected exceptions
        print(f"An error occurred: {e}")

        try:
            sentry_sdk.capture_exception(e)
        except:
            pass
        return jsonify({"error": str(e)}), 500  # Internal Server Error


if __name__ == "__main__":
    signal.signal(
        signal.SIGTERM,
        lambda sig, frame: sys.exit(0),
    )

    try:
        sentry_sdk.init(
            dsn=config("SENTRY_DSN"),
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
    except:
        pass

    app.run(host="0.0.0.0", port=int(config("PORT")))  # Run the API on port 5000
