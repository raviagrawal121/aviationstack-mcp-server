import pytest

from aviationstack_mcp_server.mcp.server import create_server


@pytest.mark.asyncio
async def test_flight_tools_are_registered() -> None:
    server = create_server()

    tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}

    assert "search_flights" in tool_names
    assert "search_historical_flights" in tool_names
    assert "get_flight_schedule" in tool_names


@pytest.mark.asyncio
async def test_flight_tool_schema_does_not_expose_context() -> None:
    server = create_server()

    tools = await server.list_tools()

    search_flights = next(tool for tool in tools if tool.name == "search_flights")

    properties = search_flights.input_schema.get("properties", {})

    assert "ctx" not in properties
    assert "query" in properties
