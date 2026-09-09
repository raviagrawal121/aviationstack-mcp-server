from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from aviationstack_mcp2.client.http import HTTPClient
from aviationstack_mcp2.config import Settings
from aviationstack_mcp2.errors import (
    AviationstackAPIError,
)
from aviationstack_mcp2.security import validate_endpoint

logger = logging.getLogger(__name__)


class AviationstackClient:
    """Asynchronous client for the Aviationstack REST API."""

    def __init__(
        self,
        settings: Settings,
        http_client: HTTPClient,
    ) -> None:
        self._settings = settings
        self._http_client = http_client

    async def get(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Perform a GET request against an Aviationstack endpoint."""

        url = self._build_url(endpoint)

        request_params = {
            "access_key": self._settings.aviationstack_api_key.get_secret_value(),
        }

        if params:
            request_params.update(
                {key: value for key, value in params.items() if value is not None}
            )

        logger.debug(
            "Sending Aviationstack request: method=%s endpoint=%s params=%s",
            "GET",
            endpoint,
            sorted(key for key in request_params if key != "access_key"),
        )

        response = await self._http_client.request(
            "GET",
            url,
            params=request_params,
        )

        logger.debug(
            "Received Aviationstack response: method=%s endpoint=%s status=%s",
            "GET",
            endpoint,
            response.status_code,
        )

        payload = self._parse_response(response)

        self._raise_for_api_error(payload)

        return payload

    async def close(self) -> None:
        logger.debug("Closing Aviationstack HTTP client")
        await self._http_client.close()

    def _build_url(self, endpoint: str) -> str:
        """Build an endpoint URL safely."""

        validate_endpoint(endpoint)
        normalized_base_url = self._settings.aviationstack_base_url.rstrip("/")
        normalized_endpoint = endpoint.strip("/")

        return f"{normalized_base_url}/{normalized_endpoint}"

    

    @staticmethod
    def _parse_response(response: Any) -> dict[str, Any]:
        """Parse an Aviationstack JSON response."""

        try:
            payload = response.json()
        except ValueError as exc:
            logger.warning("Aviationstack returned invalid JSON")
            raise AviationstackAPIError("Aviationstack returned an invalid JSON response.") from exc

        if not isinstance(payload, dict):
            logger.warning(
                "Aviationstack returned an unexpected response type: %s",
                type(payload).__name__,
            )
            raise AviationstackAPIError("Aviationstack returned an unexpected response format.")

        return payload
    
    @staticmethod
    def _raise_for_api_error(
        payload: dict[str, Any],
    ) -> None:
        """Translate Aviationstack application-level errors."""

        error = payload.get("error")

        if not isinstance(error, dict):
            return

        error_type = error.get("type")
        error_code = error.get("code")
        message = error.get("message")

        if not isinstance(error_type, str):
            error_type = "api_error"

        if not isinstance(error_code, str):
            error_code = None

        if not isinstance(message, str):
            message = "Aviationstack returned an API error."

        logger.warning(
            "Aviationstack API error: type=%s code=%s",
            error_type,
            error_code,
        )

        raise AviationstackAPIError(
            f"{error_type}: {message}",
            error_code=error_code,
        )