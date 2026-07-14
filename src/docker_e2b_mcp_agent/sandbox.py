"""E2B sandbox and MCP gateway lifecycle management."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from agents.mcp import MCPServerStreamableHttp
from e2b import AsyncSandbox

from .config import Settings


def build_mcp_config(settings: Settings) -> dict[str, dict[str, str]]:
    """Create the E2B MCP configuration using official Docker catalog keys."""

    return {
        "githubOfficial": {
            "githubPersonalAccessToken": settings.github_token,
        },
        "notion": {
            "internalIntegrationToken": settings.notion_token,
        },
    }


@asynccontextmanager
async def connect_e2b_mcp(settings: Settings) -> AsyncIterator[MCPServerStreamableHttp]:
    """Yield a connected Agents SDK MCP server and always destroy its sandbox."""

    sandbox = await AsyncSandbox.create(
        mcp=build_mcp_config(settings),
        timeout=settings.sandbox_timeout,
        api_key=settings.e2b_api_key,
    )

    try:
        mcp_token = await sandbox.get_mcp_token()
        if not mcp_token:
            raise RuntimeError("E2B did not return an MCP gateway token.")

        async with MCPServerStreamableHttp(
            name="E2B GitHub + Notion Gateway",
            params={
                "url": sandbox.get_mcp_url(),
                "headers": {"Authorization": f"Bearer {mcp_token}"},
                "timeout": 30,
                "sse_read_timeout": 300,
            },
            cache_tools_list=True,
        ) as server:
            yield server
    finally:
        await sandbox.kill()
