from typing import Any, Dict, Optional
from .responses import APIResponse
import logging


class RequestValidator:
    logger = logging.getLogger("RequestValidator")

    @staticmethod
    def validate_request_data(data: Dict[str, Any], fields: Dict[str, tuple[type, bool]]) -> Optional[tuple[dict, int]]:
        """
        Validates the request data by checking the presence and type of required fields.

        Parameters:
            data (Dict[str, Any]): The request data to validate.
            fields (Dict[str, tuple[type, bool]]): A dictionary where keys are field names and values are tuples
                                                   containing the expected type and a boolean indicating
                                                   whether the field is required.

        Returns:
            A tuple containing a JSON response and HTTP status code if validation fails, or None if validation succeeds.
        """
        RequestValidator.logger.info("Validating request data")

        if not data:
            RequestValidator.logger.warning("Request body is missing")
            return APIResponse.error(message="Request body is required", status_code=400)

        for field, (expected_type, is_required) in fields.items():
            if is_required and field not in data:
                RequestValidator.logger.warning(f"Missing required field: {field}")
                return APIResponse.error(
                    message=f"Missing required field: '{field}'", status_code=400
                )

            if field in data and not isinstance(data[field], expected_type):
                RequestValidator.logger.warning(
                    f"Incorrect type for field '{field}': expected {expected_type.__name__}, got {type(data[field]).__name__}"
                )
                return APIResponse.error(
                    message=f"Field '{field}' must be of type '{expected_type.__name__}'",
                    status_code=400
                )

        RequestValidator.logger.info("Request data validated successfully")
        return None
