import time
import json
import requests
import logging


class MLflowInferenceClient:
    def __init__(self, server_url: str, logger=None):
        """
        Initializes the MLflow inference client for a deployed model server.

        Args:
            server_url (str): The base URL of the MLflow inference server
                              (e.g., "http://127.0.0.1:5000").
            logger: Optional logger object. If not provided, a default logger is set up.
        """
        # Remove trailing slash if present and construct the prediction endpoint URL.
        self.server_url = server_url.rstrip("/")
        self.predict_url = f"{self.server_url}/invocations"

        # Set up the logger.
        if logger is None:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger("MLflowInferenceClient")
        else:
            self.logger = logger
        self.logger.info("MLflowInferenceClient initialized with URL: %s", self.server_url)

    def list_endpoints(self):
        """
        Lists available endpoints.

        Note:
            Standard MLflow model servers (e.g., started with mlflow models serve)
            do not implement an endpoint listing API. This is a placeholder.
        """
        self.logger.info("Listing endpoints is not implemented for MLflow inference server.")
        return None

    def predict(self, input_data: dict, params: dict = None):
        """
        Sends a prediction request to the MLflow inference server.

        Args:
            input_data (dict): The input data as a dictionary (e.g., a DataFrame
                               converted to JSON with 'split' orientation).
            params (dict): Optional query parameters to be appended to the request URL.

        Returns:
            dict: A dictionary containing the server's JSON response and the response time (in ms),
                  or None if an error occurred.
        """
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(input_data)
        url = self.predict_url

        # Append optional query parameters to the URL if provided.
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_string}"

        self.logger.info("Sending prediction request to URL: %s", url)
        self.logger.info("Payload: %s", payload)

        try:
            # Record the start time.
            start_time = int(time.time() * 1000)

            # Send the POST request.
            response = requests.post(url, headers=headers, data=payload)

            # Calculate the response time.
            response_time_ms = int(time.time() * 1000) - start_time

            if response.status_code == 200:
                self.logger.info("Response received in %d ms", response_time_ms)
                return {
                    "response": response.json(),
                    "response_time_ms": response_time_ms
                }
            else:
                self.logger.error("Error in prediction. Status code: %s, Response: %s",
                                  response.status_code, response.text)
                return None
        except Exception as e:
            self.logger.error("Exception during prediction: %s", str(e))
            return None
