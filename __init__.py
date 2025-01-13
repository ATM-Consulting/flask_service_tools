from .config import Config


class FlaskServiceTools:
    def __init__(self):
        self.access_control_url = Config.ACCESS_CONTROL_URL
        self.db_config = {
            "host": Config.DB_HOST,
            "port": Config.DB_PORT,
            "user": Config.DB_USER,
            "password": Config.DB_PASSWORD,
            "database": Config.DB_NAME
        }

    def get_db_config(self):
        return self.db_config

    def get_access_control_url(self):
        return self.access_control_url
