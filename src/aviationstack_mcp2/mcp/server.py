from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server import MCPServer

from aviationstack_mcp2.client.factory import create_aviationstack_client
from aviationstack_mcp2.config import get_settings
from aviationstack_mcp2.mcp.dependencies import AppContext, build_app_context
from aviationstack_mcp2.mcp.tools.aircraft import register_aircraft_tools
from aviationstack_mcp2.mcp.tools.airlines import register_airline_tools
from aviationstack_mcp2.mcp.tools.airports import register_airport_tools
from aviationstack_mcp2.mcp.tools.flights import register_flight_tools
from aviationstack_mcp2.mcp.tools.reference import register_reference_tools

from aviationstack_mcp2.mcp.prompts.aviation import (
    register_aviation_prompts,
)

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

    register_flight_tools(server)
    register_airport_tools(server)
    register_airline_tools(server)
    register_aircraft_tools(server)
    register_reference_tools(server)

    register_aviation_prompts(server)

    return server