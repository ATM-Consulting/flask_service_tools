import requests


class AuthManager:
    def __init__(self, access_control_url):
        self.access_control_url = access_control_url

    def validate_token(self, token, required_permissions):
        payload = {
            "token": token,
            "required_permissions": required_permissions
        }
        response = requests.post(f"{self.access_control_url}/validate_access_token", json=payload)
        if response.status_code == 200:
            return True
        else:
            response.raise_for_status()

# EXAMPLE
# from flask_service_tools.auth import AuthManager
#
# auth_manager = AuthManager(access_control_url="http://access_control_service")
#
# if not auth_manager.validate_token(token, required_permissions=["customer_support"]):
#     return {"error": "Unauthorized"}, 403
