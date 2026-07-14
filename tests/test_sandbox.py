from __future__ import annotations

from docker_e2b_mcp_agent.config import Settings
from docker_e2b_mcp_agent.sandbox import build_mcp_config


def test_build_mcp_config_uses_official_e2b_catalog_keys() -> None:
    settings = Settings(
        e2b_api_key="e2b_secret",
        github_token="github_secret",
        notion_token="notion_secret",
        nebius_api_key="nebius_secret",
    )

    config = build_mcp_config(settings)

    assert config == {
        "githubOfficial": {"githubPersonalAccessToken": "github_secret"},
        "notion": {"internalIntegrationToken": "notion_secret"},
    }
    assert "e2b_secret" not in str(config)
    assert "nebius_secret" not in str(config)
