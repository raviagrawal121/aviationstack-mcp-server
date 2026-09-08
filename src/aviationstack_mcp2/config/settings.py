from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "aviationstack-mcp2"
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    aviationstack_api_key: str = Field(
        ...,
        min_length=1,
    )

    aviationstack_base_url: str = Field(
        default="https://api.aviationstack.com/v1",
    )

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

    aviationstack_max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
    )

    aviationstack_retry_backoff: float = Field(
        default=0.5,
        ge=0,
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
