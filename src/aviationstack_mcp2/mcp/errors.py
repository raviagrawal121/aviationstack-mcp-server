from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar

from mcp.types import CallToolResult, TextContent

from aviationstack_mcp2.errors import (
    AviationstackAPIError,
    AviationstackAuthenticationError,
    AviationstackAuthorizationError,
    AviationstackConfigurationError,
    AviationstackError,
    AviationstackNotFoundError,
    AviationstackRateLimitError,
    AviationstackRequestError,
    AviationstackServerError,
    AviationstackTimeoutError,
)

logger = logging.getLogger(__name__)
T = TypeVar("T")


def translate_aviationstack_error(error: AviationstackError) -> str:
    """Convert an internal exception into a safe MCP-facing message."""

    if isinstance(error, AviationstackConfigurationError):
        return "Server configuration is invalid."

    if isinstance(error, AviationstackAuthenticationError):
        return "Aviationstack authentication failed."

    if isinstance(error, AviationstackAuthorizationError):
        return "Aviationstack authorization failed."

    if isinstance(error, AviationstackRateLimitError):
        return "Aviationstack rate limit exceeded."

    if isinstance(error, AviationstackNotFoundError):
        return "The requested Aviationstack resource was not found."

    if isinstance(error, AviationstackTimeoutError):
        return "The Aviationstack request timed out."

    if isinstance(error, AviationstackServerError):
        return "The Aviationstack service is temporarily unavailable."

    if isinstance(error, AviationstackAPIError):
        return "The Aviationstack API rejected the request."

    if isinstance(error, AviationstackRequestError):
        return "Unable to reach the Aviationstack API."

    return "An Aviationstack error occurred."


def mcp_error_message(error: AviationstackError) -> str:
    """Return the safe MCP-facing message for an Aviationstack error."""

    return translate_aviationstack_error(error)


def mcp_error_boundary(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    """Convert tool failures into safe MCP-facing errors."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T | CallToolResult:
        try:
            return await func(*args, **kwargs)
        except AviationstackError as exc:
            logger.error(
                "MCP tool failed error_type=%s",
                type(exc).__name__,
            )
            return CallToolResult(
                content=[TextContent(text=translate_aviationstack_error(exc))],
                isError=True,
            )
        except Exception:
            logger.exception("Unexpected MCP tool failure")
            return CallToolResult(
                content=[TextContent(text="Internal server error.")],
                isError=True,
            )

    return wrapper