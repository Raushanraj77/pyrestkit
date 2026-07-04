import logging
from pathlib import Path


class FrameworkLogger:
    """
    Singleton logger for the automation framework.
    """

    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger:
            return cls._logger

        log_directory = Path("logs")
        log_directory.mkdir(exist_ok=True)

        log_file = log_directory / "framework.log"

        logger = logging.getLogger("api-framework")
        logger.setLevel(logging.INFO)

        if logger.handlers:
            cls._logger = logger
            return logger

        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger = logger
        return logger
