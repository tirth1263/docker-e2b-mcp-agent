# Contributing

Thanks for helping improve RepoBrief. Focused bug fixes, documentation improvements, new offline tests, and narrowly scoped workflow enhancements are welcome.

## Local setup

1. Fork and clone the repository.
2. Install Python 3.13+ and `uv`.
3. Run `uv sync --all-extras`.
4. Copy `.env.example` to `.env` only if you need a real integration run.

The unit test suite must remain offline and must never require personal API keys.

## Before opening a pull request

```bash
uv run ruff check .
uv run pytest
uv build
```

Do not commit `.env`, service tokens, MCP bearer tokens, personal Notion page IDs, or fixtures copied from private repositories.

## Pull requests

- Explain the user-facing behavior being changed.
- Add or update tests for Python changes.
- Include screenshots for visible website changes.
- Keep dependency updates separate from feature changes when practical.
- Call out any new permission, external write, or credential requirement.
