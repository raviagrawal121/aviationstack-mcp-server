import pytest

from tests.integration.mcp.fakes import create_test_server


@pytest.mark.asyncio
async def test_airline_tools_are_registered() -> None:
    server = create_test_server()

    tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}

    assert "search_airlines" in tool_names


@pytest.mark.asyncio
async def test_search_airlines_schema() -> None:
    server = create_test_server()

    tools = await server.list_tools()

    search_airlines = next(tool for tool in tools if tool.name == "search_airlines")

    properties = search_airlines.input_schema.get(
        "properties",
        {},
    )

    assert "query" in properties
    assert "ctx" not in properties


@pytest.mark.asyncio
async def test_search_airlines_exposes_query_fields() -> None:
    server = create_test_server()

    tools = await server.list_tools()

    tool = next(tool for tool in tools if tool.name == "search_airlines")

    input_schema = tool.input_schema

    query_schema = input_schema["properties"]["query"]

    if "$ref" in query_schema:
        ref = query_schema["$ref"]

        # Resolve "#/$defs/AirportSearchQuery"
        definition_name = ref.rsplit("/", maxsplit=1)[-1]

        query_schema = input_schema["$defs"][definition_name]

    query_properties = query_schema.get("properties", {})

    assert "search" in query_properties
    assert "limit" in query_properties
    assert "offset" in query_properties
