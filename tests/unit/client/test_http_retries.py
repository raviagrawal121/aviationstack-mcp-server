from unittest.mock import AsyncMock

import httpx
import pytest

from aviationstack_mcp_server.client.http import HTTPClient
from aviationstack_mcp_server.config import Settings
from aviationstack_mcp_server.errors import (
    AviationstackAuthenticationError,
    AviationstackRequestError,
    AviationstackServerError,
    AviationstackTimeoutError,
)


def make_client(
    *,
    max_attempts: int = 3,
    backoff_factor: float = 0.5,
) -> HTTPClient:
    return HTTPClient(
        Settings(
            aviationstack_api_key="test-key",
            aviationstack_retry_max_attempts=max_attempts,
            aviationstack_retry_backoff_factor=backoff_factor,
        )
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [408, 429, 500, 502, 503, 504])
async def test_retryable_status_is_retried(
    status_code: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(max_attempts=2)
    request = AsyncMock(side_effect=[httpx.Response(status_code), httpx.Response(200)])
    sleep = AsyncMock()
    monkeypatch.setattr(client._client, "request", request)
    monkeypatch.setattr("aviationstack_mcp_server.client.http.asyncio.sleep", sleep)
    monkeypatch.setattr("aviationstack_mcp_server.client.http.random.uniform", lambda *_: 0)

    response = await client.request("GET", "https://example.com/flights")

    assert response.status_code == 200
    assert request.await_count == 2
    sleep.assert_awaited_once_with(0.5)


@pytest.mark.asyncio
async def test_timeout_preserves_typed_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(max_attempts=1)
    request = AsyncMock(
        side_effect=httpx.ReadTimeout(
            "timed out",
            request=httpx.Request("GET", "https://example.com/flights"),
        )
    )
    monkeypatch.setattr(client._client, "request", request)

    with pytest.raises(AviationstackTimeoutError):
        await client.request("GET", "https://example.com/flights")


@pytest.mark.asyncio
async def test_request_error_preserves_typed_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(max_attempts=1)
    request = AsyncMock(
        side_effect=httpx.ConnectError(
            "connection failed",
            request=httpx.Request("GET", "https://example.com/flights"),
        )
    )
    monkeypatch.setattr(client._client, "request", request)

    with pytest.raises(AviationstackRequestError):
        await client.request("GET", "https://example.com/flights")


@pytest.mark.asyncio
async def test_permanent_status_is_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(max_attempts=3)
    request = AsyncMock(return_value=httpx.Response(401))
    monkeypatch.setattr(client._client, "request", request)

    with pytest.raises(AviationstackAuthenticationError):
        await client.request("GET", "https://example.com/flights")

    request.assert_awaited_once()


@pytest.mark.asyncio
async def test_retry_attempts_are_total_attempts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(max_attempts=3)
    request = AsyncMock(side_effect=[httpx.Response(503), httpx.Response(503), httpx.Response(503)])
    sleep = AsyncMock()
    monkeypatch.setattr(client._client, "request", request)
    monkeypatch.setattr("aviationstack_mcp_server.client.http.asyncio.sleep", sleep)
    monkeypatch.setattr("aviationstack_mcp_server.client.http.random.uniform", lambda *_: 0)

    with pytest.raises(AviationstackServerError):
        await client.request("GET", "https://example.com/flights")

    assert request.await_count == 3
    assert [call.args[0] for call in sleep.await_args_list] == [0.5, 1.0]


@pytest.mark.asyncio
async def test_retry_after_is_capped(monkeypatch: pytest.MonkeyPatch) -> None:
    client = make_client(max_attempts=2)
    request = AsyncMock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "999999"}),
            httpx.Response(200),
        ]
    )
    sleep = AsyncMock()
    monkeypatch.setattr(client._client, "request", request)
    monkeypatch.setattr("aviationstack_mcp_server.client.http.asyncio.sleep", sleep)

    response = await client.request("GET", "https://example.com/flights")

    assert response.status_code == 200
    sleep.assert_awaited_once_with(30.0)
