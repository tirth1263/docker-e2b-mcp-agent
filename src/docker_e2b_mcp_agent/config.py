"""Application configuration loaded from environment variables."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


class ConfigurationError(ValueError):
    """Raised when required configuration is missing or invalid."""


def _as_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"Expected a boolean value, received {value!r}.")


def _as_int(value: str | None, *, default: int, name: str, minimum: int, maximum: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer.") from exc
    if not minimum <= parsed <= maximum:
        raise ConfigurationError(f"{name} must be between {minimum} and {maximum}.")
    return parsed


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated runtime settings.

    OpenAI is used for optional Agents SDK tracing. The actual agent model is
    served by Nebius Token Factory through its OpenAI-compatible endpoint.
    """

    e2b_api_key: str
    github_token: str
    notion_token: str
    nebius_api_key: str
    openai_api_key: str | None = None
    notion_parent_page_id: str | None = None
    nebius_model: str = "moonshotai/Kimi-K2.5"
    nebius_base_url: str = "https://api.tokenfactory.nebius.com/v1/"
    sandbox_timeout: int = 900
    max_turns: int = 20
    enable_tracing: bool = True

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> Settings:
        """Build settings from a mapping such as ``os.environ``."""

        required = {
            "E2B_API_KEY": "E2B sandbox access",
            "GITHUB_TOKEN": "GitHub MCP access",
            "NOTION_TOKEN": "Notion MCP access",
            "NEBIUS_API_KEY": "Nebius model access",
        }
        missing = [name for name in required if not env.get(name, "").strip()]
        if missing:
            joined = ", ".join(missing)
            raise ConfigurationError(
                f"Missing required environment variable(s): {joined}. "
                "Copy .env.example to .env and add your credentials."
            )

        base_url = env.get(
            "NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"
        ).strip()
        if not base_url.startswith("https://"):
            raise ConfigurationError("NEBIUS_BASE_URL must use HTTPS.")

        openai_key = env.get("OPENAI_API_KEY", "").strip() or None
        tracing = _as_bool(env.get("ENABLE_TRACING"), default=True)
        if tracing and not openai_key:
            tracing = False

        return cls(
            e2b_api_key=env["E2B_API_KEY"].strip(),
            github_token=env["GITHUB_TOKEN"].strip(),
            notion_token=env["NOTION_TOKEN"].strip(),
            nebius_api_key=env["NEBIUS_API_KEY"].strip(),
            openai_api_key=openai_key,
            notion_parent_page_id=env.get("NOTION_PARENT_PAGE_ID", "").strip() or None,
            nebius_model=env.get("NEBIUS_MODEL", "moonshotai/Kimi-K2.5").strip(),
            nebius_base_url=base_url,
            sandbox_timeout=_as_int(
                env.get("SANDBOX_TIMEOUT"),
                default=900,
                name="SANDBOX_TIMEOUT",
                minimum=60,
                maximum=3600,
            ),
            max_turns=_as_int(
                env.get("MAX_TURNS"),
                default=20,
                name="MAX_TURNS",
                minimum=2,
                maximum=50,
            ),
            enable_tracing=tracing,
        )

    def safe_summary(self) -> dict[str, str | int | bool]:
        """Return non-secret settings suitable for logs and diagnostics."""

        return {
            "model": self.nebius_model,
            "model_endpoint": self.nebius_base_url,
            "sandbox_timeout": self.sandbox_timeout,
            "max_turns": self.max_turns,
            "tracing_enabled": self.enable_tracing,
            "notion_parent_configured": bool(self.notion_parent_page_id),
        }
