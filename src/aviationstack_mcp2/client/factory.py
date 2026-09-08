from aviationstack_mcp2.client.aviationstack import AviationstackClient
from aviationstack_mcp2.client.http import HTTPClient
from aviationstack_mcp2.config import Settings


def create_aviationstack_client(
    settings: Settings,
) -> AviationstackClient:
    """Create a configured Aviationstack API client."""

    http_client = HTTPClient(settings)

    return AviationstackClient(
        settings=settings,
        http_client=http_client,
    )
