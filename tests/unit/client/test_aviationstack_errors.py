import httpx
import pytest

from aviationstack_mcp_server.client.aviationstack import AviationstackClient
from aviationstack_mcp_server.client.http import HTTPClient
from aviationstack_mcp_server.errors import (
    AviationstackAPIError,
    AviationstackAuthenticationError,
    AviationstackAuthorizationError,
    AviationstackNotFoundError,
    AviationstackRateLimitError,
    AviationstackRequestError,
    AviationstackServerError,
)


def response(status_code: int) -> httpx.Response:
    return httpx.Response(status_code=status_code)


# ---------------------------------------------------------------------------
# HTTP status-code mapping
# ---------------------------------------------------------------------------


def test_401_maps_to_authentication_error() -> None:
    with pytest.raises(AviationstackAuthenticationError):
        HTTPClient._raise_for_status(response(401))


def test_403_maps_to_authorization_error() -> None:
    with pytest.raises(AviationstackAuthorizationError):
        HTTPClient._raise_for_status(response(403))


def test_404_maps_to_not_found_error() -> None:
    with pytest.raises(AviationstackNotFoundError):
        HTTPClient._raise_for_status(response(404))


def test_429_maps_to_rate_limit_error() -> None:
    with pytest.raises(AviationstackRateLimitError):
        HTTPClient._raise_for_status(response(429))


@pytest.mark.parametrize("status_code", [500, 502, 503, 504])
def test_5xx_maps_to_server_error(status_code: int) -> None:
    with pytest.raises(AviationstackServerError):
        HTTPClient._raise_for_status(response(status_code))


@pytest.mark.parametrize("status_code", [400, 405, 409, 422])
def test_4xx_maps_to_request_error(status_code: int) -> None:
    with pytest.raises(AviationstackRequestError):
        HTTPClient._raise_for_status(response(status_code))


# ---------------------------------------------------------------------------
# Successful HTTP responses
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status_code", [200, 201, 204])
def test_success_status_does_not_raise(status_code: int) -> None:
    HTTPClient._raise_for_status(response(status_code))


# ---------------------------------------------------------------------------
# Structured Aviationstack API errors
# ---------------------------------------------------------------------------


def test_structured_api_error_is_mapped() -> None:
    payload = {
        "error": {
            "code": "invalid_access_key",
            "message": "Invalid access key.",
        }
    }

    with pytest.raises(
        AviationstackAPIError,
        match="Invalid access key.",
    ) as exc_info:
        AviationstackClient._raise_for_api_error(payload)

    assert exc_info.value.error_code == "invalid_access_key"


def test_structured_api_error_includes_error_type() -> None:
    payload = {
        "error": {
            "type": "authentication_error",
            "code": "invalid_access_key",
            "message": "Invalid access key.",
        }
    }

    with pytest.raises(
        AviationstackAPIError,
        match="authentication_error",
    ):
        AviationstackClient._raise_for_api_error(payload)


def test_api_error_without_code_is_handled() -> None:
    payload = {
        "error": {
            "message": "Something went wrong.",
        }
    }

    with pytest.raises(
        AviationstackAPIError,
        match="Something went wrong.",
    ) as exc_info:
        AviationstackClient._raise_for_api_error(payload)

    assert exc_info.value.error_code is None


def test_api_error_without_message_uses_fallback() -> None:
    payload = {
        "error": {
            "code": "some_error",
        }
    }

    with pytest.raises(
        AviationstackAPIError,
        match="Aviationstack returned an API error.",
    ):
        AviationstackClient._raise_for_api_error(payload)


def test_api_error_with_invalid_message_uses_fallback() -> None:
    payload = {
        "error": {
            "code": "some_error",
            "message": {"unexpected": "object"},
        }
    }

    with pytest.raises(
        AviationstackAPIError,
        match="Aviationstack returned an API error.",
    ):
        AviationstackClient._raise_for_api_error(payload)


def test_api_error_with_invalid_code_sets_none() -> None:
    payload = {
        "error": {
            "code": 12345,
            "message": "Something went wrong.",
        }
    }

    with pytest.raises(
        AviationstackAPIError,
        match="Something went wrong.",
    ) as exc_info:
        AviationstackClient._raise_for_api_error(payload)

    assert exc_info.value.error_code is None


# ---------------------------------------------------------------------------
# Malformed / unexpected API payloads
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"data": []},
        {"error": None},
        {"error": ""},
        {"error": []},
        {"error": "something went wrong"},
        {"error": 123},
    ],
)
def test_non_structured_error_payload_does_not_raise(
    payload: dict,
) -> None:
    AviationstackClient._raise_for_api_error(payload)
