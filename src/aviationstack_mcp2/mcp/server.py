from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server import MCPServer

from aviationstack_mcp2.client.factory import create_aviationstack_client
from aviationstack_mcp2.config import get_settings
from aviationstack_mcp2.mcp.dependencies import AppContext, build_app_context



@asynccontextmanager
async def app_lifespan(
    server: MCPServer[AppContext],
) -> AsyncIterator[AppContext]:
    """Initialize and clean up application-wide dependencies."""

    settings = get_settings()
    client = create_aviationstack_client(settings)

    try:
        app_context = build_app_context(client)

        yield app_context

    finally:
        await client.close()


def create_server() -> MCPServer[AppContext]:
    """Create and configure the Aviationstack MCP server."""

    server = MCPServer(
        "aviationstack-mcp",
        lifespan=app_lifespan,
    )

    return server