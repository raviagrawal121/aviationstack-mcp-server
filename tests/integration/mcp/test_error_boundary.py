import logging
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
from mcp import Client

from aviationstack_mcp2.client import AviationstackClient, HTTPClient
from aviationstack_mcp2.config import Settings
from aviationstack_mcp2.errors import AviationstackRateLimitError
from aviationstack_mcp2.logging_config import CorrelationIdFilter
from aviationstack_mcp2.mcp.server import create_server


class RateLimitFakeClient:
    """Fake client that raises a rate-limit error with sensitive details."""

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise AviationstackRateLimitError(
            "secret access_key=super-secret-value traceback=internal",
            status_code=429,
        )

    async def close(self) -> None:
        pass


@pytest.mark.asyncio
async def test_rate_limit_error_is_safe_at_mcp_boundary() -> None:
    server = create_server(client_factory=RateLimitFakeClient)

    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.call_tool(
            "search_airports",
            arguments={
                "query": {
                    "search": "London",
                    "limit": 5,
                }
            },
        )

    result_text = "\n".join(getattr(item, "text", "") for item in result.content)
    serialized_result = str(result)

    assert result.is_error is True
    assert "Aviationstack rate limit exceeded." in result_text
    for value in (result_text, serialized_result):
        assert "secret" not in value
        assert "access_key" not in value
        assert "traceback" not in value


@pytest.mark.asyncio
async def test_mcp_tool_logs_shared_correlation_id(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
        aviationstack_retry_max_attempts=1,
    )
    http_client = HTTPClient(settings)
    aviationstack_client = AviationstackClient(settings, http_client)
    response = httpx.Response(
        200,
        json={
            "data": [
                {
                    "airport_name": "Heathrow",
                    "iata_code": "LHR",
                }
            ]
        },
        request=httpx.Request("GET", "https://example.com/airports"),
    )
    request = AsyncMock(return_value=response)
    monkeypatch.setattr(http_client._client, "request", request)

    caplog.set_level(logging.DEBUG)
    correlation_filter = CorrelationIdFilter()
    caplog.handler.addFilter(correlation_filter)
    try:
        server = create_server(client_factory=lambda: aviationstack_client)

        async with Client(
            server,
            raise_exceptions=True,
        ) as client:
            result = await client.call_tool(
                "search_airports",
                arguments={
                    "query": {
                        "search": "London",
                        "limit": 5,
                    }
                },
            )
    finally:
        caplog.handler.removeFilter(correlation_filter)

    assert result.is_error is False

    request_records = [
        record
        for record in caplog.records
        if record.name
        in {
            "aviationstack_mcp2.mcp.errors",
            "aviationstack_mcp2.client.aviationstack",
            "aviationstack_mcp2.client.http",
        }
        and record.correlation_id != "-"
    ]
    mcp_ids = {
        record.correlation_id
        for record in request_records
        if record.name == "aviationstack_mcp2.mcp.errors"
    }
    http_ids = {
        record.correlation_id
        for record in request_records
        if record.name
        in {
            "aviationstack_mcp2.client.aviationstack",
            "aviationstack_mcp2.client.http",
        }
    }
    correlation_ids = mcp_ids | http_ids

    assert correlation_ids
    assert len(correlation_ids) == 1
    assert mcp_ids
    assert http_ids
