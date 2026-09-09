import pytest

from aviationstack_mcp2.config.settings import Environment
from aviationstack_mcp2.errors import (
    AviationstackAuthenticationError,
    AviationstackConfigurationError,
)
from aviationstack_mcp2.mcp.errors import translate_aviationstack_error
from aviationstack_mcp2.security import (
    redact_mapping,
    validate_api_base_url,
    validate_endpoint,
)


def test_redact_mapping_hides_sensitive_keys_case_insensitively() -> None:
    values = {
        "access_key": "secret",
        "Authorization": "Bearer secret",
        "limit": 10,
    }

    redacted = redact_mapping(values)

    assert redacted == {
        "access_key": "***REDACTED***",
        "Authorization": "***REDACTED***",
        "limit": 10,
    }
    assert values["access_key"] == "secret"


def test_production_base_url_requires_https_and_provider_host() -> None:
    with pytest.raises(AviationstackConfigurationError, match="HTTPS"):
        validate_api_base_url(
            "http://api.aviationstack.com/v1",
            environment="production",
        )

    with pytest.raises(AviationstackConfigurationError, match="host"):
        validate_api_base_url(
            "https://internal.example/v1",
            environment="production",
        )


def test_non_production_base_url_can_use_test_host() -> None:
    validate_api_base_url(
        "http://localhost:8080/v1",
        environment="testing",
    )


def test_base_url_rejects_embedded_credentials_and_query() -> None:
    with pytest.raises(AviationstackConfigurationError):
        validate_api_base_url(
            "https://user:password@api.aviationstack.com/v1?token=secret",
            environment="testing",
        )


def test_endpoint_rejects_absolute_url_and_query() -> None:
    with pytest.raises(AviationstackConfigurationError):
        validate_endpoint("https://internal.example/metadata")

    with pytest.raises(AviationstackConfigurationError):
        validate_endpoint("airports?target=internal")


def test_relative_endpoint_is_allowed() -> None:
    validate_endpoint("/airports")


def test_redact_sensitive_values():
    values = {
        "access_key": "secret",
        "limit": 10,
    }

    result = redact_mapping(values)

    assert result["access_key"] == "***REDACTED***"
    assert result["limit"] == 10


def test_redaction_is_case_insensitive():
    values = {
        "ACCESS_KEY": "secret",
        "Authorization": "Bearer secret",
    }

    result = redact_mapping(values)

    assert result["ACCESS_KEY"] == "***REDACTED***"
    assert result["Authorization"] == "***REDACTED***"


def test_api_key_not_exposed_in_error():
    error = AviationstackAuthenticationError(
        "internal secret value",
        status_code=401,
    )

    message = translate_aviationstack_error(error)

    assert "secret" not in message


def test_production_requires_https() -> None:
    with pytest.raises(AviationstackConfigurationError):
        validate_api_base_url(
            "http://api.aviationstack.com/v1",
            environment=Environment.PRODUCTION.value,
        )


def test_production_accepts_https() -> None:
    validate_api_base_url(
        "https://api.aviationstack.com/v1",
        environment=Environment.PRODUCTION.value,
    )
