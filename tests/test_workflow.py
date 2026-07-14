from __future__ import annotations

import pytest

from docker_e2b_mcp_agent.config import Settings
from docker_e2b_mcp_agent.workflow import DEFAULT_TASK, prepare_task


def make_settings(parent: str | None = None) -> Settings:
    return Settings(
        e2b_api_key="e2b",
        github_token="github",
        notion_token="notion",
        nebius_api_key="nebius",
        notion_parent_page_id=parent,
    )


def test_default_task_describes_top_three_workflow() -> None:
    assert "top 3" in DEFAULT_TASK
    assert "Notion" in DEFAULT_TASK


def test_prepare_task_adds_configured_parent() -> None:
    task = prepare_task("Create a summary", make_settings("page_123"))

    assert task.endswith("Notion parent: page_123")


def test_prepare_task_leaves_prompt_unchanged_without_parent() -> None:
    assert prepare_task("  Create a summary  ", make_settings()) == "Create a summary"


def test_prepare_task_rejects_empty_prompt() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        prepare_task("  ", make_settings())
