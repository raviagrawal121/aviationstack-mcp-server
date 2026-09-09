from __future__ import annotations

from urllib.parse import urlparse

from aviationstack_mcp2.errors import AviationstackConfigurationError

SENSITIVE_KEYS = frozenset(
    {
        "access_key",
        "api_key",
        "apikey",
        "authorization",
        "token",
        "password",
        "secret",
    }
)


def redact_mapping(
    values: dict[str, object],
) -> dict[str, object]:
    """Return a copy with sensitive values redacted."""

    return {
        key: (
            "***REDACTED***"
            if key.lower() in SENSITIVE_KEYS
            else value
        )
        for key, value in values.items()
    }


def validate_api_base_url(
    base_url: str,
    *,
    environment: str,
) -> None:
    """Enforce secure, provider-specific API URL policy in production."""

    parsed = urlparse(base_url)

    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise AviationstackConfigurationError(
            "API base URL must not contain credentials, query parameters, or fragments."
        )

    if environment == "production":
        if parsed.scheme != "https":
            raise AviationstackConfigurationError(
                "Production API base URL must use HTTPS."
            )

        if parsed.hostname != "api.aviationstack.com":
            raise AviationstackConfigurationError(
                "Production API base URL must use the Aviationstack API host."
            )


def validate_endpoint(endpoint: str) -> None:
    """Reject endpoint inputs that could turn the client into a URL proxy."""

    parsed = urlparse(endpoint)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise AviationstackConfigurationError(
            "Aviationstack endpoints must be relative paths without query parameters."
        )