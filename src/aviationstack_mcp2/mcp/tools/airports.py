import logging

from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.mcp.errors import mcp_error_boundary
from aviationstack_mcp2.models.queries import AirportSearchQuery

logger = logging.getLogger(__name__)


def register_airport_tools(server) -> None:
    """Register airport-related MCP tools."""

    @server.tool(
        name="search_airports",
        title="Search Airports",
        description=(
            "Search airports by airport name, IATA code, ICAO code, "
            "city, or other supported airport search criteria."
        ),
    )
    @mcp_error_boundary
    async def search_airports(
        query: AirportSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search airport records."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: search_airports limit=%s offset=%s search_provided=%s",
            query.limit,
            query.offset,
            query.search is not None,
        )
        records = await app.services.airport.search_airports(query)
        logger.debug(
            "MCP tool completed: search_airports returned=%s",
            len(records),
        )

        return records