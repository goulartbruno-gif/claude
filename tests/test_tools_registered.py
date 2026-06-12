"""Wiring test: assert every expected MCP tool is registered.

Runs WITHOUT a live NotebookLM/Google session — it only imports the server
module and inspects FastMCP's tool registry (the lifespan that authenticates
runs only under ``mcp.run()``, not on import). This guards against typos and
missing ``@mcp.tool()`` decorators after refactors.

Run:  pytest -q   (or)   python tests/test_tools_registered.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server

EXPECTED_TOOLS = {
    # notebooks
    "list_notebooks", "create_notebook", "rename_notebook",
    "get_notebook_summary", "get_notebook_description",
    "get_notebook_metadata", "get_notebook_share_url",
    # chat
    "ask_notebook", "configure_chat", "save_chat_answer_as_note",
    # sources
    "add_source_url", "add_source_text", "add_source_file", "add_source_drive",
    "list_sources", "get_source_fulltext", "get_source_guide", "rename_source",
    # notes
    "list_notes", "get_note", "create_note", "update_note", "delete_note",
    "note_to_source",
    # studio generation
    "generate_audio_overview", "generate_video_overview", "generate_slide_deck",
    "generate_mind_map", "generate_infographic", "generate_quiz",
    "generate_flashcards", "generate_summary_report", "generate_data_table",
    # artifacts
    "list_artifacts", "get_artifact", "wait_for_artifact", "download_artifact",
    # research
    "start_research", "wait_for_research", "import_research_sources",
}


def _registered_tool_names():
    """Return the set of tool names registered on the FastMCP instance,
    tolerant to FastMCP version differences."""
    mcp = server.mcp
    # FastMCP 2.x public async API
    if hasattr(mcp, "get_tools"):
        tools = asyncio.run(mcp.get_tools())
        return set(tools.keys())
    # Fallbacks for other versions
    tm = getattr(mcp, "_tool_manager", None)
    if tm is not None and hasattr(tm, "_tools"):
        return set(tm._tools.keys())
    raise AssertionError("Cannot introspect FastMCP tool registry")


def test_all_expected_tools_registered():
    names = _registered_tool_names()
    missing = EXPECTED_TOOLS - names
    assert not missing, f"Missing tools: {sorted(missing)}"


def test_tool_count_at_least_40():
    assert len(_registered_tool_names()) >= 40


if __name__ == "__main__":
    names = _registered_tool_names()
    missing = EXPECTED_TOOLS - names
    print(f"registered: {len(names)} tools")
    if missing:
        print("MISSING:", sorted(missing))
        raise SystemExit(1)
    print("OK — all expected tools registered")
