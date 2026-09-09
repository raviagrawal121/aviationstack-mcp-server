import logging

from aviationstack_mcp2.client.aviationstack import AviationstackClient
from aviationstack_mcp2.client.http import HTTPClient
from aviationstack_mcp2.config import Settings

logger = logging.getLogger(__name__)


def create_aviationstack_client(
    settings: Settings,
) -> AviationstackClient:
    """Create a configured Aviationstack API client."""

    logger.debug(
        "Creating Aviationstack client: base_url=%s connect_timeout=%s "
        "read_timeout=%s max_retries=%s retry_backoff=%s",
        settings.aviationstack_base_url,
        settings.aviationstack_connect_timeout,
        settings.aviationstack_read_timeout,
        settings.aviationstack_max_retries,
        settings.aviationstack_retry_backoff,
    )

    http_client = HTTPClient(settings)

    return AviationstackClient(
        settings=settings,
        http_client=http_client,
    )
