import pytest

from tests.integration.mcp.fakes import create_test_server


@pytest.mark.asyncio
async def test_aviation_prompts_are_registered() -> None:
    server = create_test_server()

    prompts = await server.list_prompts()

    prompt_names = {prompt.name for prompt in prompts}

    expected_prompts = {
        "plan_flight_search",
        "plan_schedule_search",
        "plan_reference_data_search",
    }

    assert expected_prompts.issubset(prompt_names)


@pytest.mark.asyncio
async def test_flight_search_prompt_arguments() -> None:
    server = create_test_server()

    prompts = await server.list_prompts()

    prompt = next(prompt for prompt in prompts if prompt.name == "plan_flight_search")

    argument_names = {argument.name for argument in (prompt.arguments or [])}

    assert "request" in argument_names


@pytest.mark.asyncio
async def test_schedule_prompt_arguments() -> None:
    server = create_test_server()

    prompts = await server.list_prompts()

    prompt = next(prompt for prompt in prompts if prompt.name == "plan_schedule_search")

    argument_names = {argument.name for argument in (prompt.arguments or [])}

    assert "airport" in argument_names
    assert "schedule_type" in argument_names


@pytest.mark.asyncio
async def test_flight_search_prompt_content() -> None:
    server = create_test_server()

    result = await server.get_prompt(
        "plan_flight_search",
        arguments={
            "request": "Find Emirates flights from Delhi to Dubai",
        },
    )

    text = str(result)

    assert "Emirates" in text
    assert "Delhi" in text
    assert "Dubai" in text
    assert "search_flights" in text
