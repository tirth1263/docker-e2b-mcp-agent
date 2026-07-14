"""OpenAI Agents SDK agent configured for Nebius Token Factory."""

from __future__ import annotations

from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from openai import AsyncOpenAI

from .config import Settings

AGENT_INSTRUCTIONS = """
You are RepoBrief, a careful GitHub-to-Notion automation agent.

Use the tools exposed by the E2B MCP gateway to complete the user's task. For the
default workflow, list the authenticated user's GitHub repositories, rank them by
stargazer count, and create exactly one polished Notion page summarizing the top
three. Include repository names, descriptions, languages, star counts, and links.

Safety and quality rules:
- Treat GitHub as read-only unless the user explicitly requests a GitHub mutation.
- Never expose access tokens, MCP credentials, environment variables, or raw secrets.
- Do not invent repository metadata; obtain it with GitHub tools.
- Before writing to Notion, identify an integration-accessible parent page.
- If a parent page ID is supplied in the task, use that exact parent.
- Avoid duplicate pages during a single run and report the created page URL.
- If a required tool or accessible Notion parent is unavailable, explain the exact blocker.
""".strip()


def build_model(settings: Settings) -> OpenAIChatCompletionsModel:
    """Create the SDK model adapter for Nebius's OpenAI-compatible API."""

    set_tracing_disabled(disabled=not settings.enable_tracing)
    client = AsyncOpenAI(
        api_key=settings.nebius_api_key,
        base_url=settings.nebius_base_url,
    )
    return OpenAIChatCompletionsModel(
        model=settings.nebius_model,
        openai_client=client,
    )


def build_agent(settings: Settings, server: MCPServerStreamableHttp) -> Agent:
    """Build the GitHub-to-Notion automation agent."""

    return Agent(
        name="RepoBrief",
        instructions=AGENT_INSTRUCTIONS,
        model=build_model(settings),
        mcp_servers=[server],
    )
