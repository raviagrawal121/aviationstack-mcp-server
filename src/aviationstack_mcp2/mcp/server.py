import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from mcp.server import MCPServer

from aviationstack_mcp2.client.aviationstack import AviationstackClient
from aviationstack_mcp2.client.factory import create_aviationstack_client
from aviationstack_mcp2.config import get_settings
from aviationstack_mcp2.mcp.dependencies import (
    AppContext,
    build_app_context,
)
from aviationstack_mcp2.mcp.prompts.aviation import (
    register_aviation_prompts,
)
from aviationstack_mcp2.mcp.resources.documentation import (
    register_documentation_resources,
)
from aviationstack_mcp2.mcp.resources.metadata import (
    register_metadata_resources,
)
from aviationstack_mcp2.mcp.tools.aircraft import register_aircraft_tools
from aviationstack_mcp2.mcp.tools.airlines import register_airline_tools
from aviationstack_mcp2.mcp.tools.airports import register_airport_tools
from aviationstack_mcp2.mcp.tools.flights import register_flight_tools
from aviationstack_mcp2.mcp.tools.reference import register_reference_tools

logger = logging.getLogger(__name__)

ClientFactory = Callable[[], AviationstackClient]


def default_client_factory() -> AviationstackClient:
    """Create the production Aviationstack client from application settings."""

    settings = get_settings()
    return create_aviationstack_client(settings)


def create_lifespan(
    client_factory: ClientFactory = default_client_factory,
):
    """Create the application lifespan with an injectable client factory."""

    @asynccontextmanager
    async def lifespan(
        server: MCPServer[AppContext],
    ) -> AsyncIterator[AppContext]:
        logger.info("Starting Aviationstack MCP application lifespan")
        client = client_factory()

        try:
            logger.info("Aviationstack API client initialized")

            app_context = build_app_context(client)
            logger.info("Aviationstack application context ready")

            yield app_context
        finally:
            logger.info("Shutting down Aviationstack MCP application lifespan")
            try:
                await client.close()
            except Exception:
                logger.exception("Failed to close Aviationstack API client")
                raise
            else:
                logger.info("Aviationstack API client closed")

    return lifespan


def create_server(
    client_factory: ClientFactory = default_client_factory,
) -> MCPServer[AppContext]:
    """Create and configure the Aviationstack MCP server."""

    logger.debug("Creating Aviationstack MCP server")
    server = MCPServer(
        "aviationstack-mcp",
        lifespan=create_lifespan(client_factory),
    )

    # Tools
    register_flight_tools(server)
    register_airport_tools(server)
    register_airline_tools(server)
    register_aircraft_tools(server)
    register_reference_tools(server)

    # Prompts
    register_aviation_prompts(server)

    # Resources
    register_metadata_resources(server)
    register_documentation_resources(server)

    logger.info("Aviationstack MCP server configured")
    return server


# from collections.abc import AsyncIterator
# from contextlib import asynccontextmanager

# from mcp.server import MCPServer

# from aviationstack_mcp2.client.factory import create_aviationstack_client
# from aviationstack_mcp2.config import get_settings
# from aviationstack_mcp2.mcp.dependencies import AppContext, build_app_context
# from aviationstack_mcp2.mcp.prompts.aviation import (
#     register_aviation_prompts,
# )
# from aviationstack_mcp2.mcp.resources.documentation import (
#     register_documentation_resources,
# )
# from aviationstack_mcp2.mcp.resources.metadata import (
#     register_metadata_resources,
# )
# from aviationstack_mcp2.mcp.tools.aircraft import register_aircraft_tools
# from aviationstack_mcp2.mcp.tools.airlines import register_airline_tools
# from aviationstack_mcp2.mcp.tools.airports import register_airport_tools
# from aviationstack_mcp2.mcp.tools.flights import register_flight_tools
# from aviationstack_mcp2.mcp.tools.reference import register_reference_tools


# @asynccontextmanager
# async def app_lifespan(
#     server: MCPServer[AppContext],
# ) -> AsyncIterator[AppContext]:
#     """Initialize and clean up application-wide dependencies."""

#     settings = get_settings()
#     client = create_aviationstack_client(settings)

#     try:
#         app_context = build_app_context(client)

#         yield app_context

#     finally:
#         await client.close()


# def create_server() -> MCPServer[AppContext]:
#     """Create and configure the Aviationstack MCP server."""

#     server = MCPServer(
#         "aviationstack-mcp",
#         lifespan=app_lifespan,
#     )

#     register_flight_tools(server)
#     register_airport_tools(server)
#     register_airline_tools(server)
#     register_aircraft_tools(server)
#     register_reference_tools(server)

#     register_aviation_prompts(server)

#     # Resources
#     register_metadata_resources(server)
#     register_documentation_resources(server)

#     return server
