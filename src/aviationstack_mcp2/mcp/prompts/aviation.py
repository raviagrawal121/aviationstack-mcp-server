from mcp.server.mcpserver import MCPServer


def register_aviation_prompts(server: MCPServer) -> None:
    """Register Aviationstack MCP prompts."""

    @server.prompt(
        name="plan_flight_search",
        title="Plan Flight Search",
        description=(
            "Help formulate a flight search using available "
            "Aviationstack flight filters."
        ),
    )
    def plan_flight_search(
        request: str,
    ) -> str:
        """Generate guidance for searching flights."""

        return (
            "Plan a flight search using the Aviationstack MCP server.\n\n"
            f"User request:\n{request}\n\n"
            "Determine the relevant flight filters such as airline, "
            "flight number, departure airport, arrival airport, "
            "and date. Then use the search_flights tool with the "
            "appropriate structured query."
        )

    @server.prompt(
        name="plan_schedule_search",
        title="Plan Schedule Search",
        description=(
            "Help formulate an airport arrival or departure "
            "schedule search."
        ),
    )
    def plan_schedule_search(
        airport: str,
        schedule_type: str = "departure",
    ) -> str:
        """Generate guidance for an airport schedule search."""

        return (
            "Plan an Aviationstack airport schedule lookup.\n\n"
            f"Airport: {airport}\n"
            f"Schedule type: {schedule_type}\n\n"
            "Use the get_flight_schedule tool. Ensure the airport "
            "identifier and schedule type are mapped to the "
            "corresponding structured query fields. Return the "
            "schedule information relevant to the user's request."
        )

    @server.prompt(
        name="plan_reference_data_search",
        title="Plan Reference Data Search",
        description=(
            "Help determine which Aviationstack reference-data "
            "tool should be used for a lookup."
        ),
    )
    def plan_reference_data_search(
        request: str,
    ) -> str:
        """Generate guidance for reference-data lookup."""

        return (
            "Plan a reference-data lookup using the "
            "Aviationstack MCP server.\n\n"
            f"User request:\n{request}\n\n"
            "Choose the appropriate reference-data capability:\n"
            "- list_countries for country reference data\n"
            "- list_cities for city reference data\n"
            "- search_routes for airline route data\n"
            "- search_taxes for aviation tax data\n"
            "- list_aircraft_types for aircraft type data\n"
            "- list_airplanes for individual airplane records\n\n"
            "Use the selected tool with its structured query."
        )