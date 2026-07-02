---
name: "Andromeda Dispatch"
description: "Scans the Andrômeda Obsidian vault for open tasks and routes them to ruflo agents for execution, writing results back to the vault. Use when asked to run/check/process pending vault tasks, or as a scheduled dispatch pass."
---

# Andromeda Dispatch

Bridges the `obsidian-dispatch` MCP server (reads/writes the Obsidian vault) with the
`claude-flow` MCP server (ruflo's agent orchestration) so vault notes with `type: task`
become real dispatched work, with results written back as notes.

## Prerequisites

- Both MCP servers connected in this session: `obsidian-dispatch` and `claude-flow`
  (registered in `.mcp.json`; if either is missing, ask the user to run `claude` from
  the repo root so it picks up the project config)
- `OBSIDIAN_VAULT_PATH` set to the local vault path

## Procedure

1. Call `dispatch_scan_tasks` to list every note with `type: task, status: open`.
   If the list is empty, report that and stop.
2. For each task note:
   a. Call `vault_read_note` to get the full `## Objetivo` section text.
   b. Use `ToolSearch("select:hooks_route")` (or the equivalent claude-flow routing
      tool) to load its schema before calling — the exact parameter names haven't
      been verified against a live `claude-flow` MCP session, only inferred from
      `CLAUDE.md`'s CLI examples (`hooks route --task "..."`). Confirm the schema
      first rather than assuming it matches the CLI flag names.
   c. Call the routing tool with the objective text to get an agent recommendation.
   d. Call `dispatch_mark_running(path, agent)` to record which agent picked up
      the task, before starting work.
   e. Dispatch the actual work via claude-flow's agent/task-orchestration tool
      (documented as `agent_spawn` / `task_orchestrate`) — same caveat as 2b,
      confirm its schema with `ToolSearch` before the first call.
   f. When the agent returns a result, write it to a new note (e.g.
      `Projects/Andromeda/Results/<task title>.md`) via `vault_write_note`, then
      call `dispatch_mark_done(path, result_note)` to close out the task note.
3. Summarize what was scanned, routed, and completed.

## Known unknowns

- The exact parameter schemas for claude-flow's routing/spawn tools were not
  verified while authoring this skill — the CLI wraps an MCP server
  (`npx ruflo@latest mcp start`) that only responds inside a live MCP session, so
  it couldn't be introspected standalone. Always `ToolSearch` the tool before
  calling it the first time in a real session, and update this skill once confirmed.
- Scheduling: to run this on an interval rather than on demand, either point
  ruflo's own daemon (`npx ruflo@latest daemon start`) at a headless `claude`
  session running this skill, or use Claude Code's `CronCreate` for a local session.
