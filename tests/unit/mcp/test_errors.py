from aviationstack_mcp_server.errors import (
    AviationstackAuthenticationError,
    AviationstackRateLimitError,
    AviationstackTimeoutError,
)
from aviationstack_mcp_server.mcp.errors import translate_aviationstack_error


def test_authentication_error_message() -> None:
    error = AviationstackAuthenticationError(
        "secret internal message",
        status_code=401,
    )

    assert translate_aviationstack_error(error) == "Aviationstack authentication failed."


def test_rate_limit_error_message() -> None:
    error = AviationstackRateLimitError(
        "internal details",
        status_code=429,
    )

    assert translate_aviationstack_error(error) == "Aviationstack rate limit exceeded."


def test_timeout_error_message() -> None:
    error = AviationstackTimeoutError("internal details")

    assert translate_aviationstack_error(error) == "The Aviationstack request timed out."


def test_sensitive_information_is_not_exposed() -> None:
    error = AviationstackAuthenticationError(
        "access_key=super-secret-value",
        status_code=401,
    )

    message = translate_aviationstack_error(error)

    assert "super-secret-value" not in message
    assert "access_key" not in message
