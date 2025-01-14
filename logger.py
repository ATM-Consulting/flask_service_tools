import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name, log_level="INFO", log_to_file=False, log_file_path=None, max_file_size=5 * 1024 * 1024,
                 backup_count=5):
        """
        Initialize a logger with optional file logging and rotation.

        :param name: Name of the logger (usually the module name).
        :param log_level: Logging level (e.g., DEBUG, INFO, WARNING).
        :param log_to_file: If True, logs will be written to a file.
        :param log_file_path: Path to the log file (required if log_to_file=True).
        :param max_file_size: Maximum size of the log file before rotation (in bytes).
        :param backup_count: Number of backup log files to keep.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler with rotation
        if log_to_file:
            if not log_file_path:
                raise ValueError("log_file_path is required if log_to_file is True.")
            file_handler = RotatingFileHandler(
                log_file_path, maxBytes=max_file_size, backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
