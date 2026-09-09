import logging

from mcp.server.mcpserver import MCPServer

logger = logging.getLogger(__name__)


def register_documentation_resources(server: MCPServer) -> None:
    """Register MCP documentation resources."""

    logger.debug("Registering Aviationstack documentation resources")

    @server.resource(
        "aviationstack://metadata/endpoints",
        name="aviationstack_endpoints",
        title="Aviationstack API Endpoints",
        description=(
            "Public documentation of the Aviationstack API domains used by this MCP server."
        ),
        mime_type="application/json",
    )
    def aviationstack_endpoints() -> dict[str, object]:
        """Return public endpoint documentation."""

        logger.debug("Reading documentation resource: aviationstack://metadata/endpoints")
        return {
            "flights": {
                "endpoint": "/flights",
                "operations": [
                    "search_flights",
                    "search_historical_flights",
                ],
            },
            "schedule": {
                "endpoint": "/timetable",
                "operations": [
                    "get_flight_schedule",
                ],
            },
            "future_schedule": {
                "endpoint": "/flightsFuture",
                "operations": [
                    "get_flight_schedule",
                ],
            },
            "aircraft_types": {
                "endpoint": "/aircraft_types",
                "operations": [
                    "list_aircraft_types",
                ],
            },
            "airplanes": {
                "endpoint": "/airplanes",
                "operations": [
                    "list_airplanes",
                ],
            },
            "countries": {
                "endpoint": "/countries",
                "operations": [
                    "list_countries",
                ],
            },
            "cities": {
                "endpoint": "/cities",
                "operations": [
                    "list_cities",
                ],
            },
            "airports": {
                "endpoint": "/airports",
                "operations": [
                    "search_airports",
                ],
            },
            "airlines": {
                "endpoint": "/airlines",
                "operations": [
                    "search_airlines",
                ],
            },
            "routes": {
                "endpoint": "/routes",
                "operations": [
                    "search_routes",
                ],
            },
            "taxes": {
                "endpoint": "/taxes",
                "operations": [
                    "search_taxes",
                ],
            },
        }

    @server.resource(
        "aviationstack://documentation/tools",
        name="tool_documentation",
        title="Aviationstack MCP Tools",
        description=("Documentation of the tools exposed by the Aviationstack MCP server."),
        mime_type="application/json",
    )
    def tool_documentation() -> dict[str, object]:
        """Return public MCP tool documentation."""

        logger.debug("Reading documentation resource: aviationstack://documentation/tools")
        return {
            "tools": [
                {
                    "name": "search_flights",
                    "domain": "flights",
                    "purpose": "Search flight records.",
                },
                {
                    "name": "search_historical_flights",
                    "domain": "flights",
                    "purpose": "Search historical flight records.",
                },
                {
                    "name": "get_flight_schedule",
                    "domain": "flights",
                    "purpose": "Retrieve airport flight schedules.",
                },
                {
                    "name": "search_airports",
                    "domain": "airports",
                    "purpose": "Search airport records.",
                },
                {
                    "name": "search_airlines",
                    "domain": "airlines",
                    "purpose": "Search airline records.",
                },
                {
                    "name": "list_aircraft_types",
                    "domain": "aircraft",
                    "purpose": "List aircraft type records.",
                },
                {
                    "name": "list_airplanes",
                    "domain": "aircraft",
                    "purpose": "List airplane records.",
                },
                {
                    "name": "list_countries",
                    "domain": "reference_data",
                    "purpose": "List country records.",
                },
                {
                    "name": "list_cities",
                    "domain": "reference_data",
                    "purpose": "List city records.",
                },
                {
                    "name": "search_routes",
                    "domain": "reference_data",
                    "purpose": "Search route records.",
                },
                {
                    "name": "search_taxes",
                    "domain": "reference_data",
                    "purpose": "Search aviation tax records.",
                },
            ]
        }
