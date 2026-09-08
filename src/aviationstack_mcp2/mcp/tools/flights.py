from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.models.queries import (
    AirportScheduleQuery,
    FlightSearchQuery,
    HistoricalFlightQuery,
)


def register_flight_tools(
    server,
) -> None:
    """Register flight-related MCP tools."""

    @server.tool(
        name="search_flights",
        title="Search Flights",
        description=(
            "Search flights using airline, flight number, departure, "
            "arrival, date, and pagination filters."
        ),
    )
    async def search_flights(
        query: FlightSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search scheduled flight records."""

        app = ctx.request_context.lifespan_context

        return await app.services.flight.search_flights(query)

    @server.tool(
        name="search_historical_flights",
        title="Search Historical Flights",
        description=(
            "Search historical flight records for a specific date "
            "using optional airline, flight number, departure, "
            "arrival, and pagination filters."
        ),
    )
    async def search_historical_flights(
        query: HistoricalFlightQuery,
        ctx: Context[AppContext],
    ):
        """Search historical flight records."""

        app = ctx.request_context.lifespan_context

        return await app.services.flight.get_historical_flights(query)

    @server.tool(
        name="get_flight_schedule",
        title="Get Flight Schedule",
        description=(
            "Retrieve airport arrival or departure schedules using "
            "an airport IATA code and schedule filters."
        ),
    )
    async def get_flight_schedule(
        query: AirportScheduleQuery,
        ctx: Context[AppContext],
    ):
        """Retrieve airport flight schedules."""

        app = ctx.request_context.lifespan_context

        return await app.services.flight.get_airport_schedule(query)