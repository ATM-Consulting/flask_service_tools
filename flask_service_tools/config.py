import os


class Config:
    # Service configuration
    SERVICE_NAME = os.getenv("SERVICE_NAME", "service")
    SERVICE_UUID = os.getenv("SERVICE_UUID", "service-uuid")

    # Access Control configuration
    ACCESS_CONTROL_URL = os.getenv("ACCESS_CONTROL_URL", "http://access_control_service")

    # AI gateway configuration
    AI_GATEWAY_URL = os.getenv("AI_GATEWAY_URL", "http://ai_gateway:7000")

    # Usage monitoring configuration
    UM_DB_HOST = os.getenv("UM_DB_HOST", "usage_monitoring")
    UM_DB_PORT = int(os.getenv("UM_DB_PORT", 3306))
    UM_DB_USER = os.getenv("UM_DB_USER", "client")
    UM_DB_NAME = os.getenv("UM_DB_NAME", "usage_monitoring_db")
    UM_DB_PASSWORD = open(os.getenv("UM_DB_PASSWORD_PATH", "/run/secrets/um_mysql_password")).read().strip()

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "False").lower() in ("true", "1")
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/var/log/flask_service.log")
    LOG_MAX_FILE_SIZE = int(os.getenv("LOG_MAX_FILE_SIZE", 5 * 1024 * 1024))  # Default 5MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 5))  # Default 5 backups
