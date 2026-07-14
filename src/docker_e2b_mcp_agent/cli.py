"""Command-line interface for the demo."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from dotenv import load_dotenv

from .config import ConfigurationError, Settings
from .workflow import DEFAULT_TASK, list_available_tools, run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="e2b-mcp-agent",
        description="Automate GitHub-to-Notion tasks through an E2B MCP gateway.",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_TASK,
        help="Natural-language task for the agent (defaults to the top-repositories demo).",
    )
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Validate configuration without creating a sandbox.",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="Connect to E2B and print available GitHub and Notion MCP tools.",
    )
    return parser


async def _run(args: argparse.Namespace, settings: Settings) -> int:
    if args.check_config:
        print("Configuration is valid.")
        print(json.dumps(settings.safe_summary(), indent=2))
        return 0

    if args.list_tools:
        tools = await list_available_tools(settings)
        print(f"Available MCP tools ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool}")
        return 0

    print("Starting an isolated E2B sandbox and connecting to the MCP gateway...")
    result = await run_workflow(settings, args.prompt)
    print("\nAgent result\n------------")
    print(result)
    return 0


def main(argv: list[str] | None = None) -> None:
    load_dotenv()
    args = build_parser().parse_args(argv)
    try:
        settings = Settings.from_env(os.environ)
        exit_code = asyncio.run(_run(args, settings))
    except (ConfigurationError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        raise SystemExit(130) from None
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
