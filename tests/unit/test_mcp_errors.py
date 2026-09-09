import inspect
import logging

import pytest

from aviationstack_mcp2.errors import AviationstackServerError
from aviationstack_mcp2.mcp.errors import mcp_error_boundary


@pytest.mark.asyncio
async def test_boundary_hides_unexpected_exception_details(
    caplog: pytest.LogCaptureFixture,
) -> None:
    @mcp_error_boundary
    async def operation() -> None:
        raise KeyError("pagination")

    with caplog.at_level(logging.ERROR):
        result = await operation()

    assert result.is_error is True
    result_text = result.content[0].text
    assert result_text == "Internal server error."
    assert "pagination" not in result_text
    assert "Unexpected MCP tool failure" in caplog.text
    assert "KeyError" in caplog.text


@pytest.mark.asyncio
async def test_boundary_translates_known_aviationstack_error() -> None:
    @mcp_error_boundary
    async def operation() -> None:
        raise AviationstackServerError("internal server detail")

    result = await operation()

    assert result.is_error is True
    assert result.content[0].text == ("The Aviationstack service is temporarily unavailable.")


@pytest.mark.asyncio
async def test_boundary_preserves_function_signature() -> None:
    async def operation(
        query: str,
        limit: int = 10,
    ) -> str:
        return f"{query}:{limit}"

    wrapped = mcp_error_boundary(operation)

    assert inspect.signature(wrapped) == inspect.signature(operation)
    assert await wrapped("airports", limit=5) == "airports:5"
