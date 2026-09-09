import logging

from mcp.server.mcpserver import Context

from aviationstack_mcp_server.mcp.dependencies import AppContext
from aviationstack_mcp_server.mcp.errors import mcp_error_boundary
from aviationstack_mcp_server.models.queries import (
    AirportScheduleQuery,
    FlightSearchQuery,
    HistoricalFlightQuery,
)

logger = logging.getLogger(__name__)


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
    @mcp_error_boundary
    async def search_flights(
        query: FlightSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search scheduled flight records."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: search_flights limit=%s filters=%s",
            query.limit,
            [
                field
                for field in (
                    "airline_name",
                    "airline_iata",
                    "flight_iata",
                    "flight_icao",
                    "departure_iata",
                    "arrival_iata",
                )
                if getattr(query, field) is not None
            ],
        )
        records = await app.services.flight.search_flights(query)
        logger.debug(
            "MCP tool completed: search_flights returned=%s",
            len(records),
        )

        return records

    @server.tool(
        name="search_historical_flights",
        title="Search Historical Flights",
        description=(
            "Search historical flight records for a specific date "
            "using optional airline, flight number, departure, "
            "arrival, and pagination filters."
        ),
    )
    @mcp_error_boundary
    async def search_historical_flights(
        query: HistoricalFlightQuery,
        ctx: Context[AppContext],
    ):
        """Search historical flight records."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: search_historical_flights date=%s limit=%s filters=%s",
            query.flight_date,
            query.limit,
            [
                field
                for field in ("airline_iata", "departure_iata", "arrival_iata")
                if getattr(query, field) is not None
            ],
        )
        records = await app.services.flight.get_historical_flights(query)
        logger.debug(
            "MCP tool completed: search_historical_flights returned=%s",
            len(records),
        )

        return records

    @server.tool(
        name="get_flight_schedule",
        title="Get Flight Schedule",
        description=(
            "Retrieve airport arrival or departure schedules using "
            "an airport IATA code and schedule filters."
        ),
    )
    @mcp_error_boundary
    async def get_flight_schedule(
        query: AirportScheduleQuery,
        ctx: Context[AppContext],
    ):
        """Retrieve airport flight schedules."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: get_flight_schedule airport=%s type=%s airline_filter=%s limit=%s",
            query.airport_iata,
            query.schedule_type.value,
            query.airline_name is not None,
            query.limit,
        )
        records = await app.services.flight.get_airport_schedule(query)
        logger.debug(
            "MCP tool completed: get_flight_schedule returned=%s",
            len(records),
        )

        return records
