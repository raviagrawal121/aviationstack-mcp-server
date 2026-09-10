import pytest
from mcp import Client

from aviationstack_mcp_server.mcp.server import create_server
from tests.integration.mcp.fakes import FakeAviationstackClient, create_test_server


@pytest.mark.asyncio
async def test_mcp_client_initializes() -> None:
    """Verify that the MCP client can initialize against the server."""

    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        # Assert
        assert client is not None


@pytest.mark.asyncio
async def test_tools_list() -> None:
    """Verify that the MCP server exposes the expected tools."""

    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.list_tools()

        # Extract tool names
        tool_names = {tool.name for tool in result.tools}

    # Assert
    expected_tools = {
        "search_flights",
        "search_historical_flights",
        "get_flight_schedule",
        "search_airports",
        "search_airlines",
        "list_aircraft_types",
        "list_airplanes",
        "list_countries",
        "list_cities",
        "search_routes",
        "search_taxes",
    }

    assert expected_tools.issubset(tool_names)


# @pytest.mark.asyncio
# async def test_tools_list() -> None:
#     server = create_server()

#     async with Client(
#         server,
#         raise_exceptions=True,
#     ) as client:
#         result = await client.list_tools()

#         tool_names = {
#             tool.name
#             for tool in result.tools
#         }

#         expected_tools = {
#             "search_flights",
#             "search_historical_flights",
#             "get_flight_schedule",
#             "search_airports",
#             "search_airlines",
#             "list_aircraft_types",
#             "list_airplanes",
#             "list_countries",
#             "list_cities",
#             "search_routes",
#             "search_taxes",
#         }

#         assert expected_tools.issubset(tool_names)

# @pytest.mark.asyncio
# async def test_tools_list() -> None:
#     result = await client.list_tools()

#     tool_names = {
#         tool.name
#         for tool in result.tools
#     }

#     expected_tools = {
#         "search_flights",
#         "search_historical_flights",
#         "get_flight_schedule",
#         "search_airports",
#         "search_airlines",
#         "list_aircraft_types",
#         "list_airplanes",
#         "list_countries",
#         "list_cities",
#         "search_routes",
#         "search_taxes",
#     }

#     assert expected_tools.issubset(tool_names)

# @pytest.mark.asyncio
# async def test_tools_have_descriptions() -> None:


#     # Arrange
#     server = create_server()

#     async with Client(
#         server,
#         raise_exceptions=True,
#     ) as client:
#         result = await client.list_tools()

#         tools = {
#             tool.name: tool
#             for tool in result.tools
#         }

#     expected_tools = {
#         "search_flights",
#         "search_airports",
#         "search_airlines",
#         "list_aircraft_types",
#         "list_airplanes",
#         "list_countries",
#         "list_cities",
#         "search_routes",
#         "search_taxes",
#     }

#     for name in expected_tools:
#         assert name in tools
#         assert tools[name].description


@pytest.mark.asyncio
async def test_search_airports_schema() -> None:

    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.list_tools()

        tool = next(tool for tool in result.tools if tool.name == "search_airports")

    properties = tool.input_schema.get("properties", {})

    assert "query" in properties


@pytest.mark.asyncio
async def test_search_flights_schema() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.list_tools()

        tool = next(tool for tool in result.tools if tool.name == "search_flights")

    properties = tool.input_schema.get("properties", {})

    assert "query" in properties


@pytest.mark.asyncio
async def test_context_is_not_exposed_in_tool_schema() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.list_tools()

    for tool in result.tools:
        properties = tool.input_schema.get("properties", {})

        assert "ctx" not in properties


@pytest.mark.asyncio
async def test_search_airports_end_to_end() -> None:
    fake_client = FakeAviationstackClient()

    def client_factory():
        return fake_client

    server = create_server(
        client_factory=client_factory,
    )

    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.call_tool(
            "search_airports",
            arguments={
                "query": {
                    "search": "Delhi",
                    "limit": 10,
                    "offset": 0,
                }
            },
        )

    assert not result.is_error
    assert not result.is_error
    assert result.content
    # assert result.structured_content is not None

    text = result.content[0].text

    assert "Indira Gandhi International Airport" in text
    assert '"iata_code": "DEL"' in text
    assert '"icao_code": "VIDP"' in text


@pytest.mark.asyncio
async def test_search_airports_rejects_invalid_limit() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.call_tool(
            "search_airports",
            arguments={
                "query": {
                    "search": "Delhi",
                    "limit": 9999,
                }
            },
        )

    assert result.is_error is True


@pytest.mark.asyncio
async def test_unknown_tool_fails() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.call_tool(
            "does_not_exist",
            arguments={},
        )

    assert result.is_error is True


@pytest.mark.asyncio
async def test_prompts_list() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.list_prompts()

    prompt_names = {prompt.name for prompt in result.prompts}

    expected = {
        "plan_flight_search",
        "plan_schedule_search",
        "plan_reference_data_search",
    }

    assert expected.issubset(prompt_names)


@pytest.mark.asyncio
async def test_plan_flight_search_prompt() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.get_prompt(
            "plan_flight_search",
            arguments={
                "request": "Find Emirates flights from Delhi to Dubai",
            },
        )

    assert result.messages

    prompt_text = str(result.messages)

    assert "Emirates" in prompt_text
    assert "Delhi" in prompt_text
    assert "Dubai" in prompt_text


@pytest.mark.asyncio
async def test_resources_list() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.list_resources()

    resource_uris = {str(resource.uri) for resource in result.resources}

    expected = {
        "aviationstack://metadata/server",
        "aviationstack://metadata/endpoints",
        "aviationstack://documentation/tools",
    }

    assert expected.issubset(resource_uris)


@pytest.mark.asyncio
async def test_server_metadata_resource() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.read_resource(
            "aviationstack://metadata/server",
        )

    assert result.contents


@pytest.mark.asyncio
async def test_tool_documentation_resource() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        result = await client.read_resource(
            "aviationstack://documentation/tools",
        )

    assert result.contents


@pytest.mark.asyncio
async def test_complete_mcp_surface() -> None:
    # Arrange
    server = create_test_server()

    # Act
    async with Client(
        server,
        raise_exceptions=True,
    ) as client:
        tools = await client.list_tools()
        prompts = await client.list_prompts()
        resources = await client.list_resources()

    assert len(tools.tools) >= 11
    assert len(prompts.prompts) >= 3
    assert len(resources.resources) >= 3
