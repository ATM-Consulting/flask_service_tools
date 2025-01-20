from responses import APIResponse


class APIError(Exception):
    def __init__(self, message, status_code=400, details=None):
        """
        Custom exception for API errors.
        :param message: Error message.
        :param status_code: HTTP status code.
        :param details: Additional error details.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details

    def to_response(self):
        """
        Convert the error to a standardized response.
        :return: Dict with error details.
        """
        return {
            "status": "error",
            "message": self.message,
            "details": self.details,
        }, self.status_code


def register_error_handlers(app):
    """
    Register error handlers with the Flask app.
    :param app: Flask app instance.
    """
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return error.to_response()

    @app.errorhandler(404)
    def handle_404(error):
        return APIResponse.error(
            message="The requested resource was not found.",
            status_code=404
        )

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return APIResponse.error(
            message="An unexpected error occurred.",
            details=str(error),
            status_code=500
        )
