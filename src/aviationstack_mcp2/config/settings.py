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

    # Application
    app_name: str = "aviationstack-mcp2"
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    # Aviationstack
    aviationstack_api_key: str = Field(
        ...,
        min_length=1,
    )
    aviationstack_base_url: str = Field(
        default="http://api.aviationstack.com/v1",
    )
    aviationstack_timeout: float = Field(
        default=30.0,
        gt=0,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached application settings instance."""
    return Settings()
