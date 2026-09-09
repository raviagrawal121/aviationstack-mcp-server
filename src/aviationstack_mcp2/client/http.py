from __future__ import annotations

import logging
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

logger = logging.getLogger(__name__)


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
                    attempt_number = attempt.retry_state.attempt_number
                    logger.debug(
                        "Sending HTTP request: method=%s url=%s attempt=%s params=%s",
                        method,
                        url,
                        attempt_number,
                        sorted(params) if params else [],
                    )

                    try:
                        response = await self._client.request(
                            method=method,
                            url=url,
                            params=params,
                            headers=headers,
                        )
                    except retryable_exceptions as exc:
                        logger.warning(
                            "Retryable HTTP request failure: method=%s url=%s "
                            "attempt=%s error=%s",
                            method,
                            url,
                            attempt_number,
                            exc,
                        )
                        raise

                    self._raise_for_status(response)

                    logger.debug(
                        "Received HTTP response: method=%s url=%s status=%s attempt=%s",
                        method,
                        url,
                        response.status_code,
                        attempt_number,
                    )
                    return response

        except httpx.TimeoutException as exc:
            logger.warning(
                "HTTP request timed out: method=%s url=%s error=%s",
                method,
                url,
                exc,
            )
            raise AviationstackTimeoutError("Aviationstack request timed out.") from exc

        except httpx.RequestError as exc:
            logger.warning(
                "HTTP request failed: method=%s url=%s error=%s",
                method,
                url,
                exc,
            )
            raise AviationstackRequestError(f"Aviationstack request failed: {exc}") from exc

        raise AviationstackRequestError("Aviationstack request failed unexpectedly.")

    async def close(self) -> None:
        """Close the underlying HTTP client."""

        logger.debug("Closing HTTP client")
        await self._client.aclose()

    @staticmethod
    def _raise_for_status(
        response: httpx.Response,
    ) -> None:
        status_code = response.status_code

        if status_code >= 400:
            logger.warning(
                "Aviationstack HTTP error response: status=%s",
                status_code,
            )

        if status_code == 401:
            raise AviationstackAuthenticationError(
                "Aviationstack authentication failed.",
                status_code=status_code,
            )

        if status_code == 403:
            raise AviationstackAuthorizationError(
                "Aviationstack authorization failed.",
                status_code=status_code,
            )

        if status_code == 404:
            raise AviationstackNotFoundError(
                "The requested Aviationstack resource was not found.",
                status_code=status_code,
            )

        if status_code == 429:
            raise AviationstackRateLimitError(
                "Aviationstack rate limit exceeded.",
                status_code=status_code,
            )

        if 500 <= status_code <= 599:
            raise AviationstackServerError(
                "Aviationstack returned a server error.",
                status_code=status_code,
            )

        if status_code >= 400:
            raise AviationstackRequestError(
                "Aviationstack request failed.",
                status_code=status_code,
            )