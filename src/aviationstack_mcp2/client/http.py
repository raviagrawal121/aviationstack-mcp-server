from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from aviationstack_mcp2.config import Settings
from aviationstack_mcp2.errors import (
    AviationstackAuthenticationError,
    AviationstackAuthorizationError,
    AviationstackNotFoundError,
    AviationstackRateLimitError,
    AviationstackRequestError,
    AviationstackServerError,
    AviationstackTimeoutError,
)


class HTTPClient:
    """Reusable asynchronous HTTP client with retry and timeout handling."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

        timeout = httpx.Timeout(
            connect=settings.aviationstack_connect_timeout,
            read=settings.aviationstack_read_timeout,
            write=settings.aviationstack_write_timeout,
            pool=settings.aviationstack_pool_timeout,
        )

        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "Accept": "application/json",
                "User-Agent": "aviationstack-mcp2/0.1.0",
            },
        )

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        """Execute an HTTP request with retry handling."""

        retryable_exceptions = (
            httpx.ConnectError,
            httpx.ReadError,
            httpx.WriteError,
            httpx.RemoteProtocolError,
        )

        retryer = AsyncRetrying(
            stop=stop_after_attempt(self._settings.aviationstack_max_retries + 1),
            wait=wait_exponential(
                multiplier=self._settings.aviationstack_retry_backoff,
                min=0.5,
                max=8,
            ),
            retry=retry_if_exception_type(retryable_exceptions),
            reraise=True,
        )

        try:
            async for attempt in retryer:
                with attempt:
                    response = await self._client.request(
                        method=method,
                        url=url,
                        params=params,
                        headers=headers,
                    )

                    self._raise_for_status(response)

                    return response

        except httpx.TimeoutException as exc:
            raise AviationstackTimeoutError("Aviationstack request timed out.") from exc

        except httpx.RequestError as exc:
            raise AviationstackRequestError(f"Aviationstack request failed: {exc}") from exc

        raise AviationstackRequestError("Aviationstack request failed unexpectedly.")

    async def close(self) -> None:
        """Close the underlying HTTP client."""

        await self._client.aclose()

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        """Translate HTTP status codes into application exceptions."""

        status_code = response.status_code

        if status_code in {401}:
            raise AviationstackAuthenticationError("Aviationstack authentication failed.")

        if status_code in {403}:
            raise AviationstackAuthorizationError(
                "Aviationstack authorization failed or the operation "
                "is not available for the current plan."
            )

        if status_code == 404:
            raise AviationstackNotFoundError("The requested Aviationstack resource was not found.")

        if status_code == 429:
            raise AviationstackRateLimitError("Aviationstack API rate limit exceeded.")

        if status_code >= 500:
            raise AviationstackServerError(f"Aviationstack server returned HTTP {status_code}.")

        if status_code >= 400:
            raise AviationstackRequestError(
                f"Aviationstack request failed with HTTP {status_code}."
            )
