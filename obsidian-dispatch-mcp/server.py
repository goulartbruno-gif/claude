import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import frontmatter
from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", "")).expanduser()
VALID_TYPES = {"task", "skill", "plan", "project", "area", "daily", "note"}
VALID_STATUSES = {"open", "running", "blocked", "done"}

mcp = FastMCP("ObsidianDispatch")


def _resolve(path: str) -> Path:
    root = VAULT_PATH.resolve()
    candidate = (root / path).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Path escapes vault root: {path}")
    return candidate


def _to_rel(path: Path) -> str:
    return str(path.relative_to(VAULT_PATH.resolve()))


def _matches_filter(meta: dict, filters: dict) -> bool:
    return all(meta.get(key) == value for key, value in filters.items())


def _list_notes(folder: str = "", frontmatter_filter: dict | None = None) -> list[dict]:
    base = _resolve(folder) if folder else VAULT_PATH.resolve()
    if not base.is_dir():
        raise ValueError(f"Folder not found: {folder}")
    results = []
    for md_path in sorted(base.rglob("*.md")):
        post = frontmatter.load(md_path)
        if frontmatter_filter and not _matches_filter(post.metadata, frontmatter_filter):
            continue
        results.append({
            "path": _to_rel(md_path),
            "title": post.metadata.get("title", md_path.stem),
            "frontmatter": post.metadata,
        })
    return results


def _update_frontmatter(path: str, patch: dict) -> dict:
    md_path = _resolve(path)
    if not md_path.is_file():
        raise ValueError(f"Note not found: {path}")
    if "status" in patch and patch["status"] not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {patch['status']!r}, expected one of {sorted(VALID_STATUSES)}")
    if "type" in patch and patch["type"] not in VALID_TYPES:
        raise ValueError(f"Invalid type: {patch['type']!r}, expected one of {sorted(VALID_TYPES)}")
    post = frontmatter.load(md_path)
    post.metadata.update(patch)
    post.metadata["updated"] = datetime.now(timezone.utc).isoformat()
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return post.metadata


@mcp.tool()
def vault_list_notes(folder: str = "", frontmatter_filter: dict | None = None) -> list[dict]:
    """List notes under `folder` (relative to vault root), optionally filtered by exact
    frontmatter field matches, e.g. {"type": "task", "status": "open"}."""
    return _list_notes(folder, frontmatter_filter)


@mcp.tool()
def vault_read_note(path: str) -> dict:
    """Read a note's raw body and parsed frontmatter."""
    md_path = _resolve(path)
    if not md_path.is_file():
        raise ValueError(f"Note not found: {path}")
    post = frontmatter.load(md_path)
    return {"path": path, "frontmatter": post.metadata, "content": post.content}


@mcp.tool()
def vault_search(query: str, folder: str = "") -> list[dict]:
    """Case-insensitive full-text search across note bodies and titles under `folder`."""
    base = _resolve(folder) if folder else VAULT_PATH.resolve()
    needle = query.lower()
    hits = []
    for md_path in sorted(base.rglob("*.md")):
        post = frontmatter.load(md_path)
        idx = post.content.lower().find(needle)
        if idx >= 0 or needle in md_path.stem.lower():
            snippet = post.content[max(0, idx - 60):idx + 120].strip() if idx >= 0 else post.content[:120].strip()
            hits.append({"path": _to_rel(md_path), "snippet": snippet})
    return hits


@mcp.tool()
def vault_get_backlinks(path: str) -> list[str]:
    """Return paths of notes containing a [[wikilink]] to the given note."""
    target = Path(path).stem
    pattern = re.compile(r"\[\[" + re.escape(target) + r"(\|[^\]]*)?\]\]")
    linkers = []
    for md_path in sorted(VAULT_PATH.resolve().rglob("*.md")):
        if md_path.stem == target:
            continue
        if pattern.search(md_path.read_text(encoding="utf-8")):
            linkers.append(_to_rel(md_path))
    return linkers


@mcp.tool()
def vault_write_note(path: str, content: str, frontmatter_fields: dict | None = None) -> str:
    """Create or overwrite a note with the given body and frontmatter fields."""
    md_path = _resolve(path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    post = frontmatter.Post(content, **(frontmatter_fields or {}))
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")
    logger.info(f"Wrote note: {path}")
    return path


@mcp.tool()
def vault_append_section(path: str, heading: str, content: str) -> str:
    """Append a `## heading` section with `content` to a note, creating it if missing."""
    md_path = _resolve(path)
    if md_path.is_file():
        post = frontmatter.load(md_path)
    else:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        post = frontmatter.Post("")
    post.content = post.content.rstrip("\n") + f"\n\n## {heading}\n\n{content}\n"
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return path


@mcp.tool()
def vault_update_frontmatter(path: str, patch: dict) -> dict:
    """Merge `patch` into a note's frontmatter, e.g. {"status": "done", "agent": "coder"}."""
    return _update_frontmatter(path, patch)


@mcp.tool()
def dispatch_scan_tasks() -> list[dict]:
    """List every note with type: task and status: open — the queue ruflo's dispatch consumes."""
    return _list_notes(frontmatter_filter={"type": "task", "status": "open"})


@mcp.tool()
def dispatch_mark_running(path: str, agent: str) -> dict:
    """Mark a task note as picked up by `agent`."""
    return _update_frontmatter(path, {"status": "running", "agent": agent})


@mcp.tool()
def dispatch_mark_done(path: str, result_note: str = "") -> dict:
    """Mark a task note as done, optionally linking to a result note."""
    patch = {"status": "done"}
    if result_note:
        patch["result"] = f"[[{Path(result_note).stem}]]"
    return _update_frontmatter(path, patch)


if __name__ == "__main__":
    if not VAULT_PATH.is_dir():
        logger.error(f"OBSIDIAN_VAULT_PATH is not set to a valid directory: {VAULT_PATH}")
        sys.exit(1)
    logger.info(f"Starting Obsidian Dispatch MCP server (vault: {VAULT_PATH})")
    mcp.run()
