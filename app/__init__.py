from .config import Config
from services.flask_service_tools.app.logger import Logger


class FlaskServiceTools:
    def __init__(self):
        self.access_control_url = Config.ACCESS_CONTROL_URL
        self.db_config = {
            "host": Config.UM_DB_HOST,
            "port": Config.UM_DB_PORT,
            "user": Config.UM_DB_USER,
            "password": Config.UM_DB_PASSWORD,
            "database": Config.UM_DB_NAME
        }

        self.logger = Logger(
            name=Config.SERVICE_NAME,
            log_level=Config.LOG_LEVEL,
            log_to_file=Config.LOG_TO_FILE,
            log_file_path=Config.LOG_FILE_PATH,
            max_file_size=Config.LOG_MAX_FILE_SIZE,
            backup_count=Config.LOG_BACKUP_COUNT
        ).get_logger()

    def get_db_config(self):
        return self.db_config

    def get_access_control_url(self):
        return self.access_control_url

    def get_logger(self):
        return self.logger
