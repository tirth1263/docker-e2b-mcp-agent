"""High-level workflow orchestration."""

from __future__ import annotations

from agents import Runner

from .agent import build_agent
from .config import Settings
from .sandbox import connect_e2b_mcp

DEFAULT_TASK = (
    "List my GitHub repositories, rank them by stargazer count, and create a Notion "
    "page titled 'My Top GitHub Repositories' that summarizes the top 3. Include each "
    "repository's description, primary language, star count, and GitHub link."
)


def prepare_task(prompt: str, settings: Settings) -> str:
    """Add an explicit Notion parent to the prompt when one is configured."""

    cleaned = prompt.strip()
    if not cleaned:
        raise ValueError("The task prompt cannot be empty.")
    if settings.notion_parent_page_id:
        return f"{cleaned}\n\nCreate the page under Notion parent: {settings.notion_parent_page_id}"
    return cleaned


async def list_available_tools(settings: Settings) -> list[str]:
    """Return MCP tool names without invoking the language model."""

    async with connect_e2b_mcp(settings) as server:
        tools = await server.list_tools()
        return sorted(tool.name for tool in tools)


async def run_workflow(settings: Settings, prompt: str = DEFAULT_TASK) -> str:
    """Run one automation task and return the agent's final message."""

    task = prepare_task(prompt, settings)
    async with connect_e2b_mcp(settings) as server:
        agent = build_agent(settings, server)
        result = await Runner.run(agent, task, max_turns=settings.max_turns)
    return str(result.final_output)
