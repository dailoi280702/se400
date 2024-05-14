import requests  # Import requests library for making HTTP requests
from flask import Flask, request, jsonify
from warehouse import process_data_from_db

app = Flask(__name__)


@app.route("/warehouse/process_data", methods=["POST"])
def process_data():
    """
    Triggers data processing logic on demand and sends a webhook notification.

    Returns:
        JSON: {"message": "Data processing successful!"} on success.
              JSON: {"error": "Error message"} on error.
    """

    try:
        # Extract data from request (optional)
        webhook_url = ""
        try:
            data = request.get_json()
            webhook_url = data.get("webhook_url", "")
        except:
            pass

        # Call data processing function
        process_data_from_db()

        # Check if a custom webhook URL is provided
        if webhook_url:
            # Send POST request to the custom webhook URL
            try:
                response = requests.post(
                    webhook_url, json={"message": "Data processing complete!"}
                )
                response.raise_for_status()  # Raise exception for non-2xx status codes
                print(
                    f"Webhook sent to {webhook_url} (status code: {response.status_code})"
                )
            except requests.exceptions.RequestException as e:
                print(f"Error sending webhook to {webhook_url}: {e}")
        else:
            print("No custom webhook URL provided, using default...")

            # Define your default webhook URL (replace with your actual URL)
            DEFAULT_WEBHOOK_URL = "https://your-default-webhook-endpoint.com"

            # Send POST request to the default webhook URL
            try:
                response = requests.post(
                    DEFAULT_WEBHOOK_URL,
                    json={"message": "Data processing complete (default)"},
                )
                response.raise_for_status()  # Raise exception for non-2xx status codes
                print(
                    f"Webhook sent to {DEFAULT_WEBHOOK_URL} (status code: {response.status_code})"
                )
            except requests.exceptions.RequestException as e:
                print(f"Error sending webhook to {DEFAULT_WEBHOOK_URL}: {e}")

        # Return success message
        return jsonify({"message": "Data processing successful!"})

    except Exception as e:  # Catch any unexpected exceptions
        # Log the error for debugging
        print(f"An error occurred: {e}")
        # Return error message in JSON format
        return jsonify({"error": str(e)}), 500  # Internal Server Error


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run the API on port 5000
