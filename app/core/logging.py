import logging.config
from typing import Any

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure application-wide logging from settings."""
    log_level = settings.log_level
    is_dev = settings.environment == "development"

    config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "format": "%(asctime)s | %(levelname)-8s | %(client_addr)s - %(request_line)s | %(status_code)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["stdout"],
                "level": log_level,
            },
            "uvicorn": {
                "handlers": ["stdout"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["stdout"],
                "level": "INFO" if is_dev else "WARNING",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["stdout"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)
