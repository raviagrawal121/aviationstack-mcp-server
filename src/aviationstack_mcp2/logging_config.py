from __future__ import annotations

import logging
from typing import Final

DEFAULT_LOG_FORMAT: Final = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

LOGGER_NAME: Final = "aviationstack_mcp2"


def configure_logging(level: str) -> None:
    """Configure application-wide logging.

    This function is intentionally idempotent so it can safely be called
    during application startup without creating duplicate handlers.
    """

    numeric_level = getattr(logging, level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    root_logger = logging.getLogger()

    root_logger.setLevel(numeric_level)

    if not root_logger.handlers:
        new_handler = logging.StreamHandler()
        new_handler.setLevel(numeric_level)

        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
        new_handler.setFormatter(formatter)

        root_logger.addHandler(new_handler)
    else:
        for handler in root_logger.handlers:
            handler.setLevel(numeric_level)

    logging.getLogger(LOGGER_NAME).setLevel(numeric_level)