import pytest

from aviationstack_mcp2.mcp.server import create_server


@pytest.mark.asyncio
async def test_reference_tools_are_registered() -> None:
    server = create_server()

    tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}

    expected_tools = {
        "list_countries",
        "list_cities",
        "search_routes",
        "search_taxes",
    }

    assert expected_tools.issubset(tool_names)

@pytest.mark.asyncio
async def test_reference_tools_do_not_expose_context() -> None:
    server = create_server()

    tools = await server.list_tools()

    reference_tools = {
        "list_countries",
        "list_cities",
        "search_routes",
        "search_taxes",
    }

    for name in reference_tools:
        tool = next(
            tool
            for tool in tools
            if tool.name == name
        )

        properties = tool.input_schema.get(
            "properties",
            {},
        )

        assert "ctx" not in properties

@pytest.mark.asyncio
async def test_reference_list_tools_expose_query() -> None:
    server = create_server()

    tools = await server.list_tools()

    for name in (
        "list_countries",
        "list_cities",
    ):
        tool = next(
            tool
            for tool in tools
            if tool.name == name
        )

        properties = tool.input_schema.get(
            "properties",
            {},
        )

        assert "query" in properties

@pytest.mark.asyncio
async def test_reference_search_tools_expose_query() -> None:
    server = create_server()

    tools = await server.list_tools()

    for name in (
        "search_routes",
        "search_taxes",
    ):
        tool = next(
            tool
            for tool in tools
            if tool.name == name
        )

        properties = tool.input_schema.get(
            "properties",
            {},
        )

        assert "query" in properties