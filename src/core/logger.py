import sys

from loguru import logger

from core.settings import get_settings


def configure_logger() -> None:
    """
    Configure the logger for the application.
    """
    settings = get_settings()

    # Remove the default logger
    logger.remove()

    # Add a new logger with specific settings
    logger.add(
        sys.stdout,
        level="DEBUG" if settings.debug else "INFO",
        colorize=True,
    )
