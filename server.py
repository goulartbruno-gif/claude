import inspect
import logging
import os
import sys
from contextlib import asynccontextmanager
from fastmcp import FastMCP
from notebooklm import NotebookLMClient

# Configure logging to stderr (stdout is used for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Client instance (singleton for the session)
_client = None
_client_context = None

@asynccontextmanager
async def lifespan(_app):
    """Initialize NotebookLM client on server startup."""
    global _client, _client_context
    logger.info("Starting NotebookLM MCP server...")
    try:
        # Optional explicit storage_state path (handy for containerized
        # deployments that mount a pre-seeded session); otherwise use the
        # default profile resolved from NOTEBOOKLM_HOME.
        storage = os.environ.get("NOTEBOOKLM_STORAGE_STATE")
        maybe = (NotebookLMClient.from_storage(storage) if storage
                 else NotebookLMClient.from_storage())
        _client = await maybe if inspect.isawaitable(maybe) else maybe
        _client_context = await _client.__aenter__()
        logger.info("NotebookLM client initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize NotebookLM client: {e}")
        logger.error("Please run 'uv run notebooklm login' to authenticate.")
        raise
    finally:
        if _client:
            try:
                await _client.__aexit__(None, None, None)
                logger.info("NotebookLM client closed")
            except Exception as e:
                logger.error(f"Error closing client: {e}")

# Initialize FastMCP server with lifespan
mcp = FastMCP("NotebookLM", lifespan=lifespan)

async def get_client():
    global _client
    if _client is None:
        raise RuntimeError("NotebookLM client not initialized. Please restart the server.")
    return _client


def _ser(obj):
    """Best-effort JSON-serialization of notebooklm-py model objects.

    Handles pydantic models (``model_dump``), dataclasses / plain objects
    (``__dict__``), lists, dicts and primitives — recursively. Falls back to
    ``str`` so a tool never fails just because a return type is unknown.
    """
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (list, tuple, set)):
        return [_ser(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _ser(v) for k, v in obj.items()}
    if hasattr(obj, "model_dump"):
        try:
            return _ser(obj.model_dump())
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        return {k: _ser(v) for k, v in vars(obj).items() if not k.startswith("_")}
    return str(obj)

@mcp.tool()
async def list_notebooks():
    """List all notebooks in your NotebookLM account."""
    client = await get_client()
    notebooks = await client.notebooks.list()
    # _ser is tolerant of the model's actual field set (older notebooklm-py
    # Notebook objects don't expose `source_count`).
    return [_ser(nb) for nb in notebooks]

@mcp.tool()
async def create_notebook(title: str):
    """Create a new notebook with the given title."""
    client = await get_client()
    notebook = await client.notebooks.create(title)
    return {"id": notebook.id, "title": notebook.title}

@mcp.tool()
async def add_source_url(notebook_id: str, url: str):
    """Add a website URL as a source to a notebook."""
    client = await get_client()
    source = await client.sources.add_url(notebook_id, url)
    return {"id": source.id, "title": source.title}

@mcp.tool()
async def add_source_text(notebook_id: str, title: str, text: str):
    """Add raw text as a source to a notebook."""
    client = await get_client()
    source = await client.sources.add_text(notebook_id, title, text)
    return {"id": source.id, "title": source.title}

@mcp.tool()
async def ask_notebook(notebook_id: str, question: str):
    """Ask a question grounded on the sources in a specific notebook."""
    client = await get_client()
    result = await client.chat.ask(notebook_id, question)
    return {
        "answer": getattr(result, "answer", ""),
        "references": _ser(getattr(result, "references", [])),
        "conversation_id": getattr(result, "conversation_id", None),
    }

@mcp.tool()
async def get_notebook_summary(notebook_id: str):
    """Get the summary and key insights of a notebook (via a grounded chat query)."""
    client = await get_client()
    result = await client.chat.ask(notebook_id, "Please provide a comprehensive summary and key insights of this notebook.")
    return {"summary": getattr(result, "answer", "")}

@mcp.tool()
async def generate_video_overview(notebook_id: str, instructions: str = "Create an engaging video overview of these sources."):
    """
    Generate a Video Overview artifact in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_video(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_audio_overview(notebook_id: str, instructions: str = "Create a deep dive podcast-style overview."):
    """
    Generate an Audio Overview (Deep Dive podcast) in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_audio(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_slide_deck(notebook_id: str, instructions: str = "Create a comprehensive slide deck."):
    """
    Generate a Slide Deck (PowerPoint style) in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_slide_deck(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_mind_map(notebook_id: str):
    """
    Generate an interactive Mind Map in NotebookLM.
    This creates a mind map and saves it as a note.
    """
    client = await get_client()
    result = await client.artifacts.generate_mind_map(notebook_id)
    return {"note_id": result.get("note_id"), "status": "Mind map generated and saved to notes."}

@mcp.tool()
async def generate_infographic(notebook_id: str, instructions: str = "Create an informative infographic."):
    """
    Generate an Infographic in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_infographic(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_quiz(notebook_id: str, instructions: str = "Create a quiz based on these sources."):
    """
    Generate a Quiz in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_quiz(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_flashcards(notebook_id: str, instructions: str = "Create study flashcards."):
    """
    Generate Flashcards in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_flashcards(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_summary_report(notebook_id: str, instructions: str = "Create a briefing document."):
    """
    Generate a Summary Report (Briefing Doc) in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_report(notebook_id, custom_prompt=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_data_table(notebook_id: str, instructions: str = "Extract key data into a table."):
    """
    Generate a Data Table artifact in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_data_table(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

# ---------------------------------------------------------------------------
# Notebook metadata
# ---------------------------------------------------------------------------

@mcp.tool()
async def rename_notebook(notebook_id: str, title: str):
    """Rename an existing notebook."""
    client = await get_client()
    return _ser(await client.notebooks.rename(notebook_id, title))

@mcp.tool()
async def get_notebook_description(notebook_id: str):
    """Get the AI-generated description of a notebook, including the list of
    NotebookLM's suggested follow-up questions/topics (`suggested_topics`)."""
    client = await get_client()
    return _ser(await client.notebooks.get_description(notebook_id))

@mcp.tool()
async def get_notebook_metadata(notebook_id: str):
    """Get a notebook's metadata (title, counts, timestamps, ownership)."""
    client = await get_client()
    return _ser(await client.notebooks.get_metadata(notebook_id))

@mcp.tool()
async def get_notebook_share_url(notebook_id: str):
    """Get the public share URL of a notebook."""
    client = await get_client()
    return {"share_url": await client.notebooks.get_share_url(notebook_id)}

# ---------------------------------------------------------------------------
# Chat instructions (system prompt / persona)
# ---------------------------------------------------------------------------

@mcp.tool()
async def configure_chat(notebook_id: str, custom_prompt: str = None, goal: str = None, response_length: str = None):
    """Set the chat persona / system instructions for a notebook. This steers
    the tone and analytical focus of subsequent `ask_notebook` answers.
    ``custom_prompt`` is free-form system instructions; ``goal`` and
    ``response_length`` are NotebookLM's built-in steering options."""
    client = await get_client()
    await client.chat.configure(notebook_id, goal=goal, response_length=response_length, custom_prompt=custom_prompt)
    return {"configured": True, "notebook_id": notebook_id}

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

@mcp.tool()
async def add_source_file(notebook_id: str, file_path: str):
    """Add a local file (PDF, Markdown, TXT, …) as a source to a notebook."""
    from pathlib import Path
    client = await get_client()
    return _ser(await client.sources.add_file(notebook_id, Path(file_path)))

@mcp.tool()
async def add_source_drive(notebook_id: str, file_id: str, title: str,
                           mime_type: str = "application/vnd.google-apps.document"):
    """Add a Google Drive file (Doc, Slides, …) as a source. ``file_id`` is the
    Drive file id; ``mime_type`` defaults to a Google Doc."""
    client = await get_client()
    return _ser(await client.sources.add_drive(notebook_id, file_id, title, mime_type=mime_type))

@mcp.tool()
async def list_sources(notebook_id: str):
    """List all sources in a notebook (id, title, type, status)."""
    client = await get_client()
    return _ser(await client.sources.list(notebook_id))

@mcp.tool()
async def get_source_fulltext(notebook_id: str, source_id: str):
    """Get the extracted full text of a source."""
    client = await get_client()
    return {"fulltext": await client.sources.get_fulltext(notebook_id, source_id)}

@mcp.tool()
async def get_source_guide(notebook_id: str, source_id: str):
    """Get the AI-generated guide for a source (summary + keywords)."""
    client = await get_client()
    return _ser(await client.sources.get_guide(notebook_id, source_id))

@mcp.tool()
async def rename_source(notebook_id: str, source_id: str, title: str):
    """Rename a source."""
    client = await get_client()
    return _ser(await client.sources.rename(notebook_id, source_id, title))

# ---------------------------------------------------------------------------
# Notes (read / create / update / promote)
# ---------------------------------------------------------------------------

@mcp.tool()
async def list_notes(notebook_id: str):
    """List all notes in a notebook."""
    client = await get_client()
    return _ser(await client.notes.list(notebook_id))

@mcp.tool()
async def get_note(notebook_id: str, note_id: str):
    """Get a single note's title and content."""
    client = await get_client()
    return _ser(await client.notes.get(notebook_id, note_id))

@mcp.tool()
async def create_note(notebook_id: str, title: str, content: str):
    """Create a new note in a notebook."""
    client = await get_client()
    return _ser(await client.notes.create(notebook_id, title=title, content=content))

@mcp.tool()
async def update_note(notebook_id: str, note_id: str, content: str, title: str = None):
    """Update an existing note's content (and optionally its title). If no
    title is given, the note's current title is preserved."""
    client = await get_client()
    if title is None:
        current = await client.notes.get(notebook_id, note_id)
        title = getattr(current, "title", None) or "Note"
    await client.notes.update(notebook_id, note_id, content, title)
    return {"updated": note_id, "title": title}

@mcp.tool()
async def delete_note(notebook_id: str, note_id: str):
    """Delete a note from a notebook."""
    client = await get_client()
    await client.notes.delete(notebook_id, note_id)
    return {"deleted": note_id}

@mcp.tool()
async def save_chat_answer_as_note(notebook_id: str, question: str, note_title: str = None):
    """Ask a grounded question and persist the answer as a note. Returns the
    answer, its cited sources, and the created note. Use this to capture a
    clarification while deepening the research loop."""
    client = await get_client()
    result = await client.chat.ask(notebook_id, question)
    answer = getattr(result, "answer", "") or ""
    title = note_title or (question[:80])
    note = await client.notes.create(notebook_id, title=title, content=answer)
    return {
        "note": _ser(note),
        "answer": answer,
        "references": _ser(getattr(result, "references", [])),
    }

@mcp.tool()
async def note_to_source(notebook_id: str, note_id: str, title: str = None):
    """Promote a note into a source: read the note's content and re-add it as a
    text source so NotebookLM treats it as ground truth in later turns.
    (NotebookLM has no native note->source conversion RPC.)"""
    client = await get_client()
    note = await client.notes.get(notebook_id, note_id)
    content = getattr(note, "content", None) or getattr(note, "text", "")
    src_title = title or (getattr(note, "title", None) or "Promoted note")
    source = await client.sources.add_text(notebook_id, src_title, content)
    return {"source": _ser(source), "from_note": note_id}

# ---------------------------------------------------------------------------
# Artifacts (list / status / download)
# ---------------------------------------------------------------------------

@mcp.tool()
async def list_artifacts(notebook_id: str):
    """List all studio artifacts in a notebook (audio, video, slides, …)."""
    client = await get_client()
    return _ser(await client.artifacts.list(notebook_id))

@mcp.tool()
async def get_artifact(notebook_id: str, artifact_id: str):
    """Get the status/details of a single artifact."""
    client = await get_client()
    return _ser(await client.artifacts.get(notebook_id, artifact_id))

@mcp.tool()
async def wait_for_artifact(notebook_id: str, task_id: str):
    """Block until an artifact-generation task completes; returns its status."""
    client = await get_client()
    return _ser(await client.artifacts.wait_for_completion(notebook_id, task_id))

_DOWNLOADERS = {
    "audio": "download_audio",
    "video": "download_video",
    "slide_deck": "download_slide_deck",
    "report": "download_report",
    "mind_map": "download_mind_map",
    "infographic": "download_infographic",
    "quiz": "download_quiz",
    "flashcards": "download_flashcards",
    "data_table": "download_data_table",
}

@mcp.tool()
async def download_artifact(notebook_id: str, artifact_type: str, dest_path: str, artifact_id: str = None):
    """Download a completed artifact to ``dest_path``. ``artifact_type`` is one
    of: audio, video, slide_deck, report, mind_map, infographic, quiz,
    flashcards, data_table. Pass ``artifact_id`` to pick a specific one."""
    client = await get_client()
    method_name = _DOWNLOADERS.get(artifact_type)
    if not method_name:
        raise ValueError(f"Unknown artifact_type '{artifact_type}'. "
                         f"Valid: {', '.join(_DOWNLOADERS)}")
    method = getattr(client.artifacts, method_name)
    if artifact_id is not None:
        out = await method(notebook_id, dest_path, artifact_id=artifact_id)
    else:
        out = await method(notebook_id, dest_path)
    return {"path": str(out) if out is not None else dest_path, "type": artifact_type}

# ---------------------------------------------------------------------------
# Research (web / Drive discovery -> import as sources)
# ---------------------------------------------------------------------------

@mcp.tool()
async def start_research(notebook_id: str, query: str, source: str = "web", mode: str = "fast"):
    """Start a research task for a notebook (``source`` = web/drive,
    ``mode`` = fast/deep). Returns a task_id; use `wait_for_research` then
    `import_research_sources` to ingest the results."""
    client = await get_client()
    status = await client.research.start(notebook_id, query, source=source, mode=mode)
    tid = status.get("task_id") if isinstance(status, dict) else getattr(status, "task_id", None)
    return {"task_id": tid, "status": _ser(status)}

@mcp.tool()
async def wait_for_research(notebook_id: str, task_id: str):
    """Block until a research task completes; returns the discovered candidates."""
    client = await get_client()
    return _ser(await client.research.wait_for_completion(notebook_id, task_id))

@mcp.tool()
async def import_research_sources(notebook_id: str, task_id: str):
    """Import the results of a completed research task as sources into the
    notebook. Waits for completion first, then imports the discovered sources."""
    client = await get_client()
    status = await client.research.wait_for_completion(notebook_id, task_id)
    if isinstance(status, dict):
        sources = status.get("sources", []) or []
    else:
        sources = list(getattr(status, "sources", []) or [])
    imported = await client.research.import_sources(notebook_id, task_id, sources)
    return {"imported": _ser(imported), "count": len(sources)}


if __name__ == "__main__":
    # Transport is stdio by default (Claude Desktop / Code style). Set
    # MCP_TRANSPORT=http to expose Streamable-HTTP for a containerized sidecar
    # the gateway reaches over a URL (host/port via MCP_HOST / MCP_PORT).
    transport = os.environ.get("MCP_TRANSPORT", "stdio").lower()
    if transport in ("http", "streamable-http", "streamable_http"):
        mcp.run(
            transport="streamable-http",
            host=os.environ.get("MCP_HOST", "127.0.0.1"),
            port=int(os.environ.get("MCP_PORT", "8000")),
        )
    else:
        mcp.run()
