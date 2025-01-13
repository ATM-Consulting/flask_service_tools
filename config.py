import os


class Config:
    ACCESS_CONTROL_URL = os.getenv("ACCESS_CONTROL_URL", "http://access_control_service")

    DB_HOST = os.getenv("DB_HOST", "usage_monitoring")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "client")
    DB_NAME = os.getenv("DB_NAME", "usage_monitoring_db")
    DB_PASSWORD = open(os.getenv("DB_PASSWORD_PATH", "/run/secrets/um_mysql_password")).read().strip()
