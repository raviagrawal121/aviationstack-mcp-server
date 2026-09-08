from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.models.queries import AirportSearchQuery


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
    async def search_airports(
        query: AirportSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search airport records."""

        app = ctx.request_context.lifespan_context

        return await app.services.airport.search_airports(query)