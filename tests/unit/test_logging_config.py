import pytest

from aviationstack_mcp2.logging_config import configure_logging


def test_configure_logging_accepts_valid_level() -> None:
    configure_logging("INFO")


def test_configure_logging_accepts_lowercase_level() -> None:
    configure_logging("debug")


def test_configure_logging_rejects_invalid_level() -> None:
    with pytest.raises(ValueError):
        configure_logging("INVALID")
