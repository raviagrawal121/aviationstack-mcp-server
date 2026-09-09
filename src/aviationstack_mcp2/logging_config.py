from __future__ import annotations

import logging
from typing import Final

from aviationstack_mcp2.observability import get_correlation_id

DEFAULT_LOG_FORMAT: Final = (
    "%(asctime)s | %(levelname)s | correlation_id=%(correlation_id)s | %(name)s | %(message)s"
)

LOGGER_NAME: Final = "aviationstack_mcp2"


class CorrelationIdFilter(logging.Filter):
    """Add the current correlation ID to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = get_correlation_id() or "-"
        return True


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
        new_handler.addFilter(CorrelationIdFilter())

        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
        new_handler.setFormatter(formatter)

        root_logger.addHandler(new_handler)
    else:
        for handler in root_logger.handlers:
            handler.setLevel(numeric_level)

    logging.getLogger(LOGGER_NAME).setLevel(numeric_level)
