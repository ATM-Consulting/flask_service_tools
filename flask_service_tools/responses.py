from flask import jsonify


class APIResponse:
    @staticmethod
    def success(data=None, message="", status_code=200):
        """
        Generate a standardized success response.
        :param data: The data to include in the response.
        :param message: A success message.
        :param status_code: HTTP status code (default 200).
        :return: JSON response with status code.
        """
        response = {
            "status": "success",
            "message": message,
            "data": data,
        }
        return jsonify(response), status_code

    @staticmethod
    def error(message="An error occurred", details=None, status_code=400):
        """
        Generate a standardized error response.
        :param message: The error message.
        :param details: Additional error details.
        :param status_code: HTTP status code (default 400).
        :return: JSON response with status code.
        """
        response = {
            "status": "error",
            "message": message,
            "details": details,
        }
        return jsonify(response), status_code
