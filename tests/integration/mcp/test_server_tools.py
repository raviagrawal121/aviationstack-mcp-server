import pytest

from aviationstack_mcp2.mcp.server import create_server


@pytest.mark.asyncio
async def test_registered_tools() -> None:
    server = create_server()

    tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}

    expected_tools = {
        "search_flights",
        "search_historical_flights",
        "get_flight_schedule",
        "search_airports",
        "search_airlines",
        "list_aircraft_types",
        "list_airplanes",
    }

    assert expected_tools.issubset(tool_names)