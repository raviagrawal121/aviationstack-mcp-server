import logging

from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.mcp.errors import mcp_error_boundary
from aviationstack_mcp2.models.queries import AirlineSearchQuery

logger = logging.getLogger(__name__)


def register_airline_tools(server) -> None:
    """Register airline-related MCP tools."""

    @server.tool(
        name="search_airlines",
        title="Search Airlines",
        description=(
            "Search airline records using airline name, IATA code, "
            "ICAO code, or other supported airline search criteria."
        ),
    )
    @mcp_error_boundary
    async def search_airlines(
        query: AirlineSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search airline records."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: search_airlines limit=%s offset=%s search_provided=%s",
            query.limit,
            query.offset,
            query.search is not None,
        )
        records = await app.services.airline.search_airlines(query)
        logger.debug(
            "MCP tool completed: search_airlines returned=%s",
            len(records),
        )

        return records