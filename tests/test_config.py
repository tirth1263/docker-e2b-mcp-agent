from __future__ import annotations

import pytest

from docker_e2b_mcp_agent.config import ConfigurationError, Settings

BASE_ENV = {
    "E2B_API_KEY": "e2b_test",
    "GITHUB_TOKEN": "github_test",
    "NOTION_TOKEN": "notion_test",
    "NEBIUS_API_KEY": "nebius_test",
}


def test_settings_load_required_credentials() -> None:
    settings = Settings.from_env(BASE_ENV)

    assert settings.nebius_model == "moonshotai/Kimi-K2.5"
    assert settings.enable_tracing is False
    assert settings.sandbox_timeout == 900
    assert "e2b_test" not in str(settings.safe_summary())


def test_openai_key_enables_tracing_by_default() -> None:
    settings = Settings.from_env({**BASE_ENV, "OPENAI_API_KEY": "openai_test"})

    assert settings.enable_tracing is True


def test_tracing_can_be_disabled_explicitly() -> None:
    settings = Settings.from_env(
        {**BASE_ENV, "OPENAI_API_KEY": "openai_test", "ENABLE_TRACING": "false"}
    )

    assert settings.enable_tracing is False


@pytest.mark.parametrize("missing", BASE_ENV)
def test_missing_required_credentials_are_reported(missing: str) -> None:
    env = {key: value for key, value in BASE_ENV.items() if key != missing}

    with pytest.raises(ConfigurationError, match=missing):
        Settings.from_env(env)


@pytest.mark.parametrize(
    ("name", "value"),
    [("SANDBOX_TIMEOUT", "59"), ("SANDBOX_TIMEOUT", "nope"), ("MAX_TURNS", "51")],
)
def test_invalid_numeric_settings_are_rejected(name: str, value: str) -> None:
    with pytest.raises(ConfigurationError):
        Settings.from_env({**BASE_ENV, name: value})


def test_non_https_model_endpoint_is_rejected() -> None:
    with pytest.raises(ConfigurationError, match="HTTPS"):
        Settings.from_env({**BASE_ENV, "NEBIUS_BASE_URL": "http://example.test/v1"})
