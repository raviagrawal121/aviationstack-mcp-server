from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

correlation_id: ContextVar[str] = ContextVar(
    "correlation_id",
    default="",
)


def generate_correlation_id() -> str:
    """Generate a correlation ID for an operation."""

    return uuid4().hex


def get_correlation_id() -> str:
    """Return the current correlation ID."""

    return correlation_id.get()


def set_correlation_id(value: str) -> None:
    """Set the current correlation ID."""

    correlation_id.set(value)