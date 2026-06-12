# NotebookLM MCP — Streamable-HTTP sidecar image.
#
# Runtime uses notebooklm-py's HTTP client driven by a pre-seeded
# storage_state.json (mounted at $NOTEBOOKLM_STORAGE_STATE), so NO browser /
# Chromium is needed at run time — only `notebooklm login` (done out of band)
# needs a browser. That keeps this image small.
FROM python:3.13-slim

# uv for fast, lockfile-faithful installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies first (better layer caching), then the project.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev

# Default to the containerized HTTP transport; override via compose env.
ENV MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8766 \
    NOTEBOOKLM_STORAGE_STATE=/opt/data/notebooklm-py/storage_state.json

EXPOSE 8766

CMD ["uv", "run", "--no-sync", "python", "server.py"]
