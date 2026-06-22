# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin that wraps Google NotebookLM as an MCP server using FastMCP. Users can manage notebooks, add sources, and generate artifacts (podcasts, videos, slides, mind maps, quizzes, flashcards, reports, data tables) through natural language.

## Development Commands

```bash
uv sync                        # Install dependencies (creates .venv)
uv run python server.py        # Start the MCP server (stdio transport)
uv run notebooklm login        # Authenticate with Google/NotebookLM (browser-based)
```

There are no tests or linting configured in this project.

## Architecture

**`server.py`** — The entire MCP server in one file. A FastMCP app with a lifespan handler that initializes a singleton `NotebookLMClient` (from `notebooklm-py`) on startup. All `@mcp.tool()` functions call `get_client()` to access this singleton, then delegate to `client.notebooks`, `client.sources`, `client.chat`, or `client.artifacts`. Logging goes to stderr because stdout is reserved for the MCP stdio protocol.

**Plugin packaging** — `.claude-plugin/plugin.json` is the plugin manifest; `.mcp.json` defines how Claude Code launches the server (`uv run python server.py` with `cwd` set to `${CLAUDE_PLUGIN_ROOT}`).

**Skills** — `.agents/skills/` contains marketing skills installed from `coreyhaines31/marketingskills` (tracked in `skills-lock.json`). `SKILL.md` at the repo root describes the NotebookLM assistant workflow.

**`config/mcporter.json`** — Configures an Exa search MCP server as an additional backend.

## Key Dependencies

- `fastmcp` — MCP server framework (defines tools via `@mcp.tool()` decorators)
- `notebooklm-py[browser]` — Python client for NotebookLM API; the `[browser]` extra enables browser-based auth via Playwright

## Authentication

NotebookLM requires browser-based Google authentication. Session state is stored locally (excluded via `.gitignore`: `storage_state.json`, `.notebooklm/`). The server will fail to start if not authenticated — the lifespan handler logs the error and raises.
