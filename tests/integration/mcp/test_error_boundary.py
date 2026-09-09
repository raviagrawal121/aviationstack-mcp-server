from typing import Any

import pytest
from mcp import Client

from aviationstack_mcp2.errors import AviationstackRateLimitError
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

    result_text = "\n".join(
        getattr(item, "text", "")
        for item in result.content
    )
    serialized_result = str(result)

    assert result.is_error is True
    assert "Aviationstack rate limit exceeded." in result_text
    for value in (result_text, serialized_result):
        assert "secret" not in value
        assert "access_key" not in value
        assert "traceback" not in value
