import requests


class AuthManager:
    def __init__(self, access_control_url):
        self.access_control_url = access_control_url

    def validate_token(self, authorization_header, required_permissions):
        if not authorization_header:
            return False, {"message" : "Authorization header must be set"}

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return False, {"message" : "Authorization header must be in the format 'Bearer _TOKEN_"}

        payload = {
            "token": parts[1],
            "required_permissions": required_permissions
        }
        response = requests.post(f"{self.access_control_url}/validate_access_token", json=payload)
        data = response.json()
        if response.status_code == 200:
            return True, data
        return False, data
