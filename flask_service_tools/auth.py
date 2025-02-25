import requests

class AuthManager:
    def __init__(self, access_control_url):
        self.access_control_url = access_control_url

    def validate_token(self, authorization_header, required_permissions):
        if not authorization_header:
            return False, {"message": "Authorization header must be set"}

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return False, {"message": "Authorization header must be in the format 'Bearer _TOKEN_"}

        payload = {
            "token": parts[1],
            "required_permissions": required_permissions
        }

        try:
            response = requests.post(
                f"{self.access_control_url}/validate_access_token",
                json=payload,
            )
            data = response.json()
            return True, data

        except requests.exceptions.HTTPError as http_err:
            return False, {"message": f"HTTP error occurred: {http_err}", "status_code": response.status_code}

        except requests.exceptions.ConnectionError:
            return False, {"message": "Failed to connect to the access control service. Please check the URL or service availability."}

        except requests.exceptions.Timeout:
            return False, {"message": "Request timed out. The access control service may be slow or unavailable."}

        except requests.exceptions.RequestException as err:
            return False, {"message": f"An unexpected error occurred: {err}"}

        except ValueError:
            return False, {"message": "Invalid response from the access control service. Could not parse JSON."}
