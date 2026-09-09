from __future__ import annotations


class AviationstackError(Exception):
    """Base exception for all Aviationstack application errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self) -> str:
        return self.message


class AviationstackConfigurationError(AviationstackError):
    """Raised when the Aviationstack client is incorrectly configured."""


class AviationstackRequestError(AviationstackError):
    """Raised when an HTTP request to Aviationstack fails."""


class AviationstackAuthenticationError(AviationstackRequestError):
    """Raised when Aviationstack rejects the API credentials."""


class AviationstackAuthorizationError(AviationstackRequestError):
    """Raised when the configured plan does not permit an operation."""


class AviationstackRateLimitError(AviationstackRequestError):
    """Raised when the Aviationstack API rate limit is exceeded."""


class AviationstackNotFoundError(AviationstackRequestError):
    """Raised when the requested Aviationstack resource is unavailable."""


class AviationstackServerError(AviationstackRequestError):
    """Raised when Aviationstack returns a server-side error."""


class AviationstackTimeoutError(AviationstackRequestError):
    """Raised when an Aviationstack request times out."""


class AviationstackAPIError(AviationstackRequestError):
    """Raised when Aviationstack returns an application-level API error."""
