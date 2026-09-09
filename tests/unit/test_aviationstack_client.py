from unittest.mock import AsyncMock, Mock

import pytest

from aviationstack_mcp_server.client import AviationstackClient, HTTPClient
from aviationstack_mcp_server.config import Settings


def test_aviationstack_client_builds_correctly() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
    )

    http_client = HTTPClient(settings)

    client = AviationstackClient(
        settings=settings,
        http_client=http_client,
    )

    assert client is not None


@pytest.mark.asyncio
async def test_client_unwraps_api_key_only_for_http_request() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
    )
    http_client = AsyncMock()
    response = Mock()
    response.json.return_value = {"data": []}
    http_client.request.return_value = response
    client = AviationstackClient(settings, http_client)

    await client.get("airports")

    http_client.request.assert_awaited_once_with(
        "GET",
        "https://api.aviationstack.com/v1/airports",
        params={"access_key": "test-key"},
    )
