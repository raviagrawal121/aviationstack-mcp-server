from __future__ import annotations


class AviationstackError(Exception):
    """Base exception for the Aviationstack MCP application."""


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
