from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import pytest_asyncio
from mcp import Client

from tests.integration.mcp.fakes import create_test_server


@asynccontextmanager
async def connected_mcp_client() -> AsyncIterator[Client]:
    """Create an MCP server and connect an in-memory MCP client."""
    server = create_test_server()

    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        yield client


@pytest_asyncio.fixture
async def mcp_client() -> AsyncIterator[Client]:
    """Provide an MCP client for integration tests."""
    async with connected_mcp_client() as client:
        yield client


# from collections.abc import AsyncIterator

# import pytest_asyncio
# from mcp import Client

# from aviationstack_mcp_server.mcp.server import create_server


# # @pytest_asyncio.fixture
# # async def mcp_client() -> AsyncIterator[Client]:
# #     """Provide an in-memory MCP client connected to the server."""

# #     server = create_server()

# #     async with Client(server, raise_exceptions=True) as client:
# #         yield client

# @pytest_asyncio.fixture
# async def mcp_client() -> AsyncIterator[Client]:
#     """Provide an in-memory MCP client connected to the server."""
#     server = create_server()

#     client = Client(
#         server,
#         raise_exceptions=True,
#     )

#     await client.__aenter__()

#     try:
#         yield client
#     finally:
#         await client.__aexit__(None, None, None)
