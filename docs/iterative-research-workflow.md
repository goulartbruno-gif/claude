# Iterative Deep-Research Workflow with NotebookLM (MCP)

This document describes an end-to-end, agent-driven research loop on top of the
NotebookLM MCP server, and doubles as the **acceptance-test scenario** for the
expanded tool set. Every step maps to a concrete MCP tool and the underlying
`notebooklm-py` method.

## Goal

Drive NotebookLM as an autonomous research partner: create a notebook, seed it
with sources, steer it with chat instructions, then **iteratively** mine
NotebookLM's own suggested follow-up questions to deepen the analysis to a fixed
depth — without re-asking the same thing — and finally fold the findings back in
as sources and produce media (audio / video / infographic).

## The loop (refined)

```
create notebook
  └─ add source(s)
       └─ set chat instructions (system prompt) for the topic / analysis goal
            └─ get overview (audio overview or a grounded summary)
                 └─ LOOP (depth = N):
                 │     1. read NotebookLM's suggested follow-up questions
                 │     2. drop questions already asked (dedup by normalized text)
                 │     3. pick 1..k unanswered questions
                 │     4. ask each → save the answer as a note
                 │     5. collect NEW suggestions surfaced by those answers
                 │     └─ go deeper until depth N or no new suggestions
                 ├─ (optional) formulate a web/Drive research query → add new sources
                 ├─ convert the most valuable notes into sources ("promote notes")
                 └─ generate Audio + Video + Infographic from the enriched notebook
```

## Step-by-step → tool mapping

| # | Step | MCP tool | `notebooklm-py` method | Notes |
|---|------|----------|------------------------|-------|
| 1 | Create notebook | `create_notebook(title)` | `notebooks.create` | returns `id` |
| 2 | Add source | `add_source_url` / `add_source_file` / `add_source_drive` / `add_source_text` | `sources.add_*` | YouTube auto-detected by `add_url` |
| 2b | Wait until source is processed | `list_sources` (poll) | `sources.list` / `wait_until_ready` | sources need processing before good answers |
| 3 | **System prompt / persona** | `configure_chat(notebook_id, instructions)` | `chat.configure` | steers tone + analytical focus |
| 4 | Overview | `generate_audio_overview` (+ `wait_for_artifact`) or `ask_notebook("summarize…")` | `artifacts.generate_audio` / `chat.ask` | audio is async → poll |
| 5 | **Read suggested follow-ups** | `get_notebook_description(notebook_id)` | `notebooks.get_description` → `suggested_topics` | NotebookLM's own proposed questions |
| 6 | Ask a chosen question, capture as note | `save_chat_answer_as_note(notebook_id, question)` | `notes.create_from_chat` | answer is grounded + persisted as a note |
| 6b | (or ask without saving) | `ask_notebook` | `chat.ask` | returns answer + cited sources |
| 7 | Iterate suggestions per note | repeat #5–#6 | — | dedup + depth control (below) |
| 8 | Research new sources | `start_research` → `wait_for_research` → `import_research_sources` | `research.start/wait_for_completion/import_sources` | web/Drive discovery |
| 9 | **Promote notes → sources** | `note_to_source(notebook_id, note_id)` | `notes.get` + `sources.add_text` | no native convert; read note, add as text source |
| 10 | Generate media | `generate_audio_overview`, `generate_video_overview`, `generate_infographic` | `artifacts.generate_*` | async → `wait_for_artifact` |
| 11 | Download outputs | `download_artifact(notebook_id, type, dest)` | `artifacts.download_*` | audio/video/infographic/report/… |
| 12 | Inspect notes / sources | `list_notes`, `get_note`, `list_sources`, `get_source_fulltext`, `get_source_guide` | `notes.*`, `sources.*` | for verification + dedup |

## Augmentations (orchestration logic — agent side)

These are not single tools; they are the control logic the agent runs around the
tools.

- **Depth control.** Keep a `depth` counter; stop the loop at `depth == N`
  (default 3). Each accepted suggestion that is asked increments the branch depth.
- **No repeated clarifications.** Maintain a set of *normalized* asked questions
  (lowercased, stripped, punctuation-collapsed). Before asking, drop any
  suggestion whose normalized form is already in the set. This is what prevents
  the loop from circling the same clarification.
- **Branching vs. breadth.** At each node you may pick `k` suggestions
  (breadth) and recurse on each (depth). Cap total questions per run to bound
  cost (NotebookLM free tier ≈ 50 queries/day).
- **Stop conditions.** Stop early when: (a) no *new* (post-dedup) suggestions
  appear, (b) depth budget reached, or (c) query budget reached.
- **Note hygiene.** Title each note as `[d{depth}] {question}` so the tree of
  clarifications is reconstructable from `list_notes`.
- **Promotion policy.** Only `note_to_source` the notes you want NotebookLM to
  treat as ground truth in later turns (promoted notes re-enter retrieval).

## Capability notes (verified against `notebooklm-py`)

- **System prompt** = `chat.configure(notebook_id, instructions=…)` (sets the
  chat persona / analytical focus). There is no separate "system prompt" object.
- **Suggested follow-up questions** come from
  `notebooks.get_description(...).suggested_topics` (and, per source,
  `sources.get_guide(...)` returns a summary + keywords). NotebookLM does not
  return suggestions inline in every chat answer, so re-query the description
  after new notes/sources to refresh them.
- **Note → source** has no native "convert" RPC: read the note
  (`notes.get`) and re-add its content with `sources.add_text`. The
  `note_to_source` tool wraps this.
- **Async artifacts.** All `generate_*` return a `task_id`; poll with
  `wait_for_artifact` before `download_artifact`.

## Acceptance-test sequence

Run this to validate the MCP after the tool additions (see `tests/`):

1. `create_notebook("MCP smoke test")` → capture `nb`.
2. `add_source_url(nb, "<a stable article or YouTube URL>")`; poll `list_sources(nb)`
   until the source is ready.
3. `configure_chat(nb, "You are a critical analyst. Focus on assumptions and counter-evidence.")`.
4. `ask_notebook(nb, "Give a 5-bullet overview.")` → expect grounded answer + sources.
5. `get_notebook_description(nb)` → expect non-empty `suggested_topics`.
6. `save_chat_answer_as_note(nb, <one suggested question>)` → expect a new note id.
7. `list_notes(nb)` / `get_note(nb, <id>)` → expect the saved note content.
8. `note_to_source(nb, <id>)` → expect a new source; `list_sources(nb)` shows it.
9. `generate_infographic(nb)` → `wait_for_artifact(nb, task_id)` →
   `download_artifact(nb, "infographic", "<dest>.png")` → file exists.
10. (optional) `start_research(nb, "<query>")` → `wait_for_research` →
    `import_research_sources` → new sources appear.

A passing run exercises notebooks, sources, chat+instructions, description
(suggestions), notes (read/create/promote), artifacts (generate/wait/download),
and research — i.e. the full loop above.
