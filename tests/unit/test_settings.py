from aviationstack_mcp2.config import Settings


def test_settings_with_required_api_key():
    settings = Settings(
        aviationstack_api_key="test-key",
    )

    assert settings.aviationstack_api_key == "test-key"
    assert settings.aviationstack_timeout == 30.0
    assert settings.log_level == "INFO"


def test_settings_custom_values():
    settings = Settings(
        aviationstack_api_key="test-key",
        aviationstack_base_url="https://example.com/v1",
        aviationstack_timeout=10,
        environment="test",
        log_level="DEBUG",
    )

    assert settings.aviationstack_base_url == "https://example.com/v1"
    assert settings.aviationstack_timeout == 10
    assert settings.environment == "test"
    assert settings.log_level == "DEBUG"
