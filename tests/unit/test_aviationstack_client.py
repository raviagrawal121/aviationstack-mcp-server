from aviationstack_mcp2.client import AviationstackClient, HTTPClient
from aviationstack_mcp2.config import Settings


def test_aviationstack_client_builds_correctly() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
    )

    http_client = HTTPClient(settings)

    client = AviationstackClient(
        settings=settings,
        http_client=http_client,
    )

    assert client is not None
