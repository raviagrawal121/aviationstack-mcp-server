import os

import pytest
from mcp import Client
from pydantic import ValidationError

from aviationstack_mcp2.config import Settings
from aviationstack_mcp2.mcp.server import create_server


@pytest.mark.live_api
@pytest.mark.asyncio
async def test_live_search_flights() -> None:
    """Exercise the real MCP-to-Aviationstack request path."""

    if os.getenv("AVIATIONSTACK_LIVE") != "1":
        pytest.skip("Set AVIATIONSTACK_LIVE=1 to run live API tests.")

    try:
        Settings()
    except ValidationError:
        pytest.skip("Live API configuration is unavailable; set AVIATIONSTACK_API_KEY.")

    server = create_server()

    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.call_tool(
            "search_flights",
            arguments={
                "query": {
                    "limit": 1,
                }
            },
        )

    result_text = "\n".join(getattr(item, "text", "") for item in result.content)
    if result.is_error and (
        "authentication failed" in result_text.lower()
        or "authorization failed" in result_text.lower()
    ):
        pytest.skip("The configured Aviationstack key is not authorized for live flights.")

    assert result.is_error is False
    assert result.content
