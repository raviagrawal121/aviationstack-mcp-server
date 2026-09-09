import pytest
from pydantic import ValidationError

from aviationstack_mcp2.config import Environment, Settings

# ---------------------------------------------------------------------------
# Basic configuration
# ---------------------------------------------------------------------------


def test_valid_settings() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
    )

    assert settings.environment == Environment.DEVELOPMENT
    assert settings.log_level == "INFO"
    assert settings.aviationstack_api_key.get_secret_value() == "test-key"


def test_default_environment_is_development() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
    )

    assert settings.environment == Environment.DEVELOPMENT


# ---------------------------------------------------------------------------
# API key validation
# ---------------------------------------------------------------------------


def test_empty_api_key_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="",
        )


def test_whitespace_api_key_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="   ",
        )


def test_tab_only_api_key_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="\t\t",
        )


def test_api_key_is_secret() -> None:
    settings = Settings(
        aviationstack_api_key="super-secret",
    )

    assert "super-secret" not in str(settings.aviationstack_api_key)


def test_api_key_can_be_retrieved_explicitly() -> None:
    settings = Settings(
        aviationstack_api_key="super-secret",
    )

    assert (
        settings.aviationstack_api_key.get_secret_value()
        == "super-secret"
    )


# ---------------------------------------------------------------------------
# Environment validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "environment",
    [
        Environment.DEVELOPMENT,
        Environment.TESTING,
        Environment.STAGING,
        Environment.PRODUCTION,
    ],
)
def test_valid_environments(environment: Environment) -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
        environment=environment,
    )

    assert settings.environment == environment


def test_invalid_environment_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            environment="prodution",
        )


# ---------------------------------------------------------------------------
# Base URL validation
# ---------------------------------------------------------------------------


def test_valid_base_url() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
        aviationstack_base_url="https://example.com/v1",
    )

    assert str(settings.aviationstack_base_url) == (
        "https://example.com/v1"
    )


@pytest.mark.parametrize(
    "base_url",
    [
        "not-a-url",
        "ftp://example.com",
        "example.com",
    ],
)
def test_invalid_base_url_rejected(base_url: str) -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            aviationstack_base_url=base_url,
        )


# ---------------------------------------------------------------------------
# HTTP timeout validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "field_name",
    [
        "aviationstack_connect_timeout",
        "aviationstack_read_timeout",
        "aviationstack_write_timeout",
        "aviationstack_pool_timeout",
    ],
)
def test_http_timeout_must_be_positive(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            **{field_name: 0},
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "aviationstack_connect_timeout",
        "aviationstack_read_timeout",
        "aviationstack_write_timeout",
        "aviationstack_pool_timeout",
    ],
)
def test_negative_http_timeout_rejected(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            **{field_name: -1},
        )


# ---------------------------------------------------------------------------
# Retry configuration
# ---------------------------------------------------------------------------


def test_zero_retries_is_allowed() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
        aviationstack_max_retries=0,
    )

    assert settings.aviationstack_max_retries == 0


def test_retry_attempts_above_maximum_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            aviationstack_max_retries=11,
        )


def test_negative_retry_attempts_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            aviationstack_max_retries=-1,
        )


def test_retry_backoff_cannot_be_negative() -> None:
    with pytest.raises(ValidationError):
        Settings(
            aviationstack_api_key="test-key",
            aviationstack_retry_backoff=-1,
        )


def test_zero_retry_backoff_is_allowed() -> None:
    settings = Settings(
        aviationstack_api_key="test-key",
        aviationstack_retry_backoff=0,
    )

    assert settings.aviationstack_retry_backoff == 0
