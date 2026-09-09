import pytest

from aviationstack_mcp2.mcp.server import create_server


@pytest.mark.asyncio
async def test_resources_are_registered() -> None:
    server = create_server()

    resources = await server.list_resources()

    resource_uris = {
        str(resource.uri)
        for resource in resources
    }

    expected_resources = {
        "aviationstack://metadata/server",
        "aviationstack://metadata/endpoints",
        "aviationstack://documentation/tools",
    }

    assert expected_resources.issubset(resource_uris)


@pytest.mark.asyncio
async def test_server_metadata_resource() -> None:
    server = create_server()

    contents = await server.read_resource(
        "aviationstack://metadata/server",
    )

    assert contents

@pytest.mark.asyncio
async def test_server_metadata_contains_project_name() -> None:
    server = create_server()

    contents = await server.read_resource(
        "aviationstack://metadata/server",
    )

    text = "\n".join(
        content.content
        for content in contents
        if isinstance(content.content, str)
    )

    assert "aviationstack_mcp2" in text
    assert "AVIATIONSTACK_API_KEY" not in text
    assert "access_key" not in text
    assert "super-secret" not in text

@pytest.mark.asyncio
async def test_endpoint_documentation_resource() -> None:
    server = create_server()

    contents = await server.read_resource(
        "aviationstack://metadata/endpoints",
    )

    assert contents

    text = "\n".join(
        content.content
        for content in contents
        if isinstance(content.content, str)
    )

    assert "AVIATIONSTACK_API_KEY" not in text
    assert "access_key" not in text

@pytest.mark.asyncio
async def test_tool_documentation_resource() -> None:
    server = create_server()

    contents = await server.read_resource(
        "aviationstack://documentation/tools",
    )

    assert contents

    text = "\n".join(
        content.content
        for content in contents
        if isinstance(content.content, str)
    )

    assert "AVIATIONSTACK_API_KEY" not in text
    assert "access_key" not in text