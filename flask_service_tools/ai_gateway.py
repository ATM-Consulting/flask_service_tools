import time

from mlflow.deployments import get_deploy_client


class AIGatewayClient:
    def __init__(self, gateway_url: str, logger):
        self.client = get_deploy_client(gateway_url)
        self.logger = logger
        self.logger.info("AIGatewayClient initialized with URL: %s", gateway_url)

    def list_endpoints(self):
        try:
            endpoints = self.client.list_endpoints()
            self.logger.info("Successfully retrieved endpoints.")
            return endpoints
        except Exception as e:
            self.logger.error("Error while listing endpoints: %s", str(e))
            return None

    def chat_predict(self, endpoint: str, messages: list):
        try:
            self.logger.info("Sending prediction request to endpoint: %s", endpoint)
            start_time = int(time.time() * 1000)
            response = self.client.query(
                endpoint=endpoint,
                inputs={"messages": messages},
            )
            response_time_ms = int(time.time() * 1000) - start_time
            self.logger.info(f"Response received successfully : {response}")
            return {
                "response": response.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "model": response.get("model", ""),
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms
            }
        except Exception as e:
            self.logger.error("Error during prediction: %s", str(e))
            return None
