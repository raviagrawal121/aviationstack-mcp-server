from __future__ import annotations

import logging
from enum import StrEnum
from functools import lru_cache

from pydantic import (
    AnyHttpUrl,
    Field,
    SecretStr,
    TypeAdapter,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from aviationstack_mcp_server.security import validate_api_base_url

_http_url_adapter = TypeAdapter(AnyHttpUrl)

logger = logging.getLogger(__name__)


class Environment(StrEnum):
    """Supported application environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "aviationstack-mcp-server"

    environment: Environment = Environment.DEVELOPMENT

    log_level: str = Field(
        default="INFO",
    )

    # ------------------------------------------------------------------
    # Aviationstack
    # ------------------------------------------------------------------

    aviationstack_api_key: SecretStr = Field(
        ...,
        min_length=1,
    )

    aviationstack_base_url: str = Field(
        default="https://api.aviationstack.com/v1",
    )

    # ------------------------------------------------------------------
    # HTTP client
    # ------------------------------------------------------------------

    aviationstack_connect_timeout: float = Field(
        default=5.0,
        gt=0,
    )

    aviationstack_read_timeout: float = Field(
        default=30.0,
        gt=0,
    )

    aviationstack_write_timeout: float = Field(
        default=30.0,
        gt=0,
    )

    aviationstack_pool_timeout: float = Field(
        default=5.0,
        gt=0,
    )

    # ------------------------------------------------------------------
    # Retry configuration
    # ------------------------------------------------------------------

    aviationstack_retry_max_attempts: int = Field(
        default=3,
        ge=1,
        le=10,
    )

    aviationstack_retry_backoff_factor: float = Field(
        default=0.5,
        ge=0,
    )

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("aviationstack_api_key")
    @classmethod
    def validate_api_key(
        cls,
        value: SecretStr,
    ) -> SecretStr:
        """Reject empty or whitespace-only API keys."""

        if not value.get_secret_value().strip():
            raise ValueError("AVIATIONSTACK_API_KEY must not be empty.")

        return value

    @field_validator("aviationstack_base_url")
    @classmethod
    def validate_base_url(cls, value: str) -> str:
        """Ensure the base URL is a valid HTTP/HTTPS URL."""

        _http_url_adapter.validate_python(value)

        return value

    @model_validator(mode="after")
    def validate_environment_security(self) -> Settings:
        """Apply stricter API URL policy to production configuration."""

        validate_api_base_url(
            self.aviationstack_base_url,
            environment=self.environment.value,
        )
        return self


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""

    settings = Settings()
    logger.debug(
        "Loaded Aviationstack settings: environment=%s log_level=%s "
        "base_url=%s connect_timeout=%s read_timeout=%s max_retries=%s "
        "retry_backoff=%s",
        settings.environment,
        settings.log_level,
        settings.aviationstack_base_url,
        settings.aviationstack_connect_timeout,
        settings.aviationstack_read_timeout,
        settings.aviationstack_retry_max_attempts,
        settings.aviationstack_retry_backoff_factor,
    )

    return settings
