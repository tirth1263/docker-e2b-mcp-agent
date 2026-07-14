from __future__ import annotations

from docker_e2b_mcp_agent.cli import build_parser
from docker_e2b_mcp_agent.workflow import DEFAULT_TASK


def test_cli_uses_demo_task_by_default() -> None:
    args = build_parser().parse_args([])

    assert args.prompt == DEFAULT_TASK
    assert args.check_config is False


def test_cli_accepts_custom_prompt() -> None:
    args = build_parser().parse_args(["--prompt", "List repositories", "--list-tools"])

    assert args.prompt == "List repositories"
    assert args.list_tools is True
