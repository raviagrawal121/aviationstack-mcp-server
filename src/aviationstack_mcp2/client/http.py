from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import Mapping
from time import perf_counter
from typing import Any

import httpx

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

MAX_RETRY_DELAY = 30.0
RETRYABLE_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})


def is_retryable_status(status_code: int) -> bool:
    """Return whether an HTTP status represents a transient failure."""

    return status_code in RETRYABLE_STATUS_CODES


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

        max_attempts = self._settings.aviationstack_retry_max_attempts
        endpoint = httpx.URL(url).path or "/"

        for attempt_number in range(1, max_attempts + 1):
            started_at = perf_counter()
            logger.debug(
                "HTTP request started method=%s endpoint=%s attempt=%s params=%s",
                method,
                endpoint,
                attempt_number,
                sorted(
                    key
                    for key in params
                    if key != "access_key"
                ) if params else [],
            )

            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=headers,
                )
            except httpx.TimeoutException as exc:
                duration_ms = (perf_counter() - started_at) * 1000
                if attempt_number >= max_attempts:
                    logger.error(
                        "HTTP request failed after %s attempts: method=%s endpoint=%s "
                        "error_type=%s duration_ms=%.2f",
                        max_attempts,
                        method,
                        endpoint,
                        type(exc).__name__,
                        duration_ms,
                    )
                    raise AviationstackTimeoutError(
                        "Aviationstack request timed out."
                    ) from exc

                await self._sleep_before_retry(
                    attempt_number,
                    method=method,
                    url=url,
                )
                continue
            except httpx.RequestError as exc:
                duration_ms = (perf_counter() - started_at) * 1000
                if attempt_number >= max_attempts:
                    logger.error(
                        "HTTP request failed after %s attempts: method=%s endpoint=%s "
                        "error_type=%s duration_ms=%.2f",
                        max_attempts,
                        method,
                        endpoint,
                        type(exc).__name__,
                        duration_ms,
                    )
                    raise AviationstackRequestError(
                        "Unable to reach the Aviationstack API."
                    ) from exc

                await self._sleep_before_retry(
                    attempt_number,
                    method=method,
                    url=url,
                )
                continue

            duration_ms = (perf_counter() - started_at) * 1000
            logger.debug(
                "HTTP response received method=%s endpoint=%s status=%s "
                "attempt=%s duration_ms=%.2f",
                method,
                endpoint,
                response.status_code,
                attempt_number,
                duration_ms,
            )

            if is_retryable_status(response.status_code):
                if attempt_number >= max_attempts:
                    logger.error(
                        "HTTP request failed after %s attempts: method=%s endpoint=%s "
                        "status=%s duration_ms=%.2f",
                        max_attempts,
                        method,
                        endpoint,
                        response.status_code,
                        duration_ms,
                    )
                    self._raise_for_status(response)

                await self._sleep_before_retry(
                    attempt_number,
                    method=method,
                    url=url,
                    response=response,
                )
                continue

            self._raise_for_status(response)
            return response

        raise AviationstackRequestError("Aviationstack request failed unexpectedly.")

    async def _sleep_before_retry(
        self,
        attempt_number: int,
        *,
        method: str,
        url: str,
        response: httpx.Response | None = None,
    ) -> None:
        """Wait before a retry using Retry-After or capped jittered backoff."""

        retry_after = self._retry_after_seconds(response)
        if retry_after is not None:
            delay = min(retry_after, MAX_RETRY_DELAY)
            retry_after_detail = f" retry_after={delay}"
        else:
            base_delay = min(
                self._settings.aviationstack_retry_backoff_factor
                * (2 ** (attempt_number - 1)),
                MAX_RETRY_DELAY,
            )
            jitter = random.uniform(0, base_delay * 0.1)
            delay = min(base_delay + jitter, MAX_RETRY_DELAY)
            retry_after_detail = ""

        logger.warning(
            "Retrying HTTP request: method=%s endpoint=%s attempt=%s delay=%.3f%s",
            method,
            httpx.URL(url).path or "/",
            attempt_number + 1,
            delay,
            retry_after_detail,
        )
        await asyncio.sleep(delay)

    @staticmethod
    def _retry_after_seconds(response: httpx.Response | None) -> float | None:
        """Parse a non-negative numeric Retry-After header, if present."""

        if response is None:
            return None

        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            return None

        try:
            delay = float(retry_after)
        except ValueError:
            return None

        return delay if delay >= 0 else None

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