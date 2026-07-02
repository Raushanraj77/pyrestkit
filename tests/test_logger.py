from src.core.logger import FrameworkLogger


def test_logger_creation() -> None:
    logger = FrameworkLogger.get_logger()

    logger.info("Framework logger initialized successfully.")

    assert logger is not None
