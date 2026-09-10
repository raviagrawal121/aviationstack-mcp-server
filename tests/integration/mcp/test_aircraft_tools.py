import pytest

from tests.integration.mcp.fakes import create_test_server


@pytest.mark.asyncio
async def test_aircraft_tools_are_registered() -> None:
    server = create_test_server()

    tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}

    assert "list_aircraft_types" in tool_names
    assert "list_airplanes" in tool_names


@pytest.mark.asyncio
async def test_aircraft_tools_do_not_expose_context() -> None:
    server = create_test_server()

    tools = await server.list_tools()

    for name in (
        "list_aircraft_types",
        "list_airplanes",
    ):
        tool = next(tool for tool in tools if tool.name == name)

        properties = tool.input_schema.get(
            "properties",
            {},
        )

        assert "ctx" not in properties


@pytest.mark.asyncio
async def test_aircraft_tools_expose_limit() -> None:
    server = create_test_server()

    tools = await server.list_tools()

    for name in (
        "list_aircraft_types",
        "list_airplanes",
    ):
        tool = next(tool for tool in tools if tool.name == name)

        input_schema = tool.input_schema

        query_schema = input_schema["properties"]["query"]

        if "$ref" in query_schema:
            ref = query_schema["$ref"]

            # Resolve "#/$defs/AirportSearchQuery"
            definition_name = ref.rsplit("/", maxsplit=1)[-1]

            query_schema = input_schema["$defs"][definition_name]

        query_properties = query_schema.get("properties", {})

        assert "limit" in query_properties
