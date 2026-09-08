from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.models.queries import AirlineSearchQuery


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
    async def search_airlines(
        query: AirlineSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search airline records."""

        app = ctx.request_context.lifespan_context

        return await app.services.airline.search_airlines(query)