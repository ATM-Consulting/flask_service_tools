import requests


class AuthManager:
    def __init__(self, access_control_url):
        self.access_control_url = access_control_url

    def validate_token(self, authorization_header, required_permissions):
        if not authorization_header:
            return False, "Authorization header must be set"

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return False, "Authorization header must be in the format 'Bearer _TOKEN_"

        payload = {
            "token": parts[1],
            "required_permissions": required_permissions
        }
        response = requests.post(f"{self.access_control_url}/validate_access_token", json=payload)
        data = response.json()
        if response.status_code == 200:
            return True, data.get('user_uuid', "")
        else:
            return False, data.get('message', "")

# EXAMPLE
# from flask_service_tools.auth import AuthManager
#
# auth_manager = AuthManager(access_control_url="http://access_control_service")
#
# if not auth_manager.validate_token(token, required_permissions=["customer_support"]):
#     return {"error": "Unauthorized"}, 403
