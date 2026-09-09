from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from aviationstack_mcp2.client.http import HTTPClient
from aviationstack_mcp2.config import Settings
from aviationstack_mcp2.errors import (
    AviationstackAPIError,
)


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
            "access_key": self._settings.aviationstack_api_key,
        }

        if params:
            request_params.update(
                {key: value for key, value in params.items() if value is not None}
            )

        response = await self._http_client.request(
            "GET",
            url,
            params=request_params,
        )

        payload = self._parse_response(response)

        self._raise_for_api_error(payload)

        return payload

    async def close(self) -> None:
        await self._http_client.close()


    def _build_url(self, endpoint: str) -> str:
        """Build an endpoint URL safely."""

        normalized_base_url = self._settings.aviationstack_base_url.rstrip("/")
        normalized_endpoint = endpoint.strip("/")

        return f"{normalized_base_url}/{normalized_endpoint}"

    

    @staticmethod
    def _parse_response(response: Any) -> dict[str, Any]:
        """Parse an Aviationstack JSON response."""

        try:
            payload = response.json()
        except ValueError as exc:
            raise AviationstackAPIError("Aviationstack returned an invalid JSON response.") from exc

        if not isinstance(payload, dict):
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

        raise AviationstackAPIError(
            f"{error_type}: {message}",
            error_code=error_code,
        )