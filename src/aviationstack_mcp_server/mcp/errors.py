from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from time import perf_counter
from typing import Any, TypeVar

from mcp.types import CallToolResult, TextContent

from aviationstack_mcp_server.errors import (
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
from aviationstack_mcp_server.observability import (
    generate_correlation_id,
    set_correlation_id,
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
) -> Callable[..., Awaitable[T | CallToolResult]]:
    """Convert tool failures into safe MCP-facing errors."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T | CallToolResult:
        tool_name = func.__name__
        correlation = generate_correlation_id()
        set_correlation_id(correlation)
        started_at = perf_counter()
        logger.info("MCP tool started tool=%s", tool_name)

        try:
            result = await func(*args, **kwargs)
            duration_ms = (perf_counter() - started_at) * 1000
            logger.info(
                "MCP tool completed tool=%s duration_ms=%.2f",
                tool_name,
                duration_ms,
            )
            return result
        except AviationstackError as exc:
            duration_ms = (perf_counter() - started_at) * 1000
            logger.error(
                "MCP tool failed tool=%s duration_ms=%.2f error_type=%s",
                tool_name,
                duration_ms,
                type(exc).__name__,
            )
            return CallToolResult(
                content=[TextContent(text=translate_aviationstack_error(exc))],
                is_error=True,
            )
        except Exception:
            duration_ms = (perf_counter() - started_at) * 1000
            logger.exception(
                "Unexpected MCP tool failure tool=%s duration_ms=%.2f",
                tool_name,
                duration_ms,
            )
            return CallToolResult(
                content=[TextContent(text="Internal server error.")],
                is_error=True,
            )
        finally:
            set_correlation_id("")

    return wrapper
