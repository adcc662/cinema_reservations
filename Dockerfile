# syntax=docker/dockerfile:1.9

# ---------------------------------------------------------------------------
# Stage 1: builder — resolve and install dependencies with uv (from uv.lock)
# ---------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# UV_COMPILE_BYTECODE  -> precompile .pyc at build time for faster cold starts
# UV_LINK_MODE=copy    -> copy packages into the venv (avoids cache-hardlink warnings)
# UV_PYTHON_DOWNLOADS  -> use the image's Python, don't fetch another one
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install ONLY dependencies first. Bind-mounting the lockfiles (instead of
# COPY) keeps them out of this layer, so the cached dependency layer is only
# invalidated when uv.lock or pyproject.toml actually change — not on every
# source edit. --no-install-project: don't install our own package yet.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Now bring in the source and install the project itself.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------------------------------------------------------------------------
# Stage 2: runtime — slim image that still ships uv, as requested
# ---------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS runtime

# Run as a non-root user. Never run production containers as root.
RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app

# Copy the fully built app (including the .venv) from the builder stage.
COPY --from=builder --chown=app:app /app /app

# Put the project's virtualenv on PATH so `uvicorn`/`alembic` resolve directly.
# HOME: Docker's USER directive does NOT export $HOME, so without this uv falls
#       back to a relative `.cache/uv` under the workdir.
# UV_CACHE_DIR: point uv's cache at a writable absolute path. /tmp is
#       world-writable, so the non-root `app` user can always create it. With
#       --no-sync at runtime nothing is installed, this is just scratch space.
ENV PATH="/app/.venv/bin:$PATH" \
    HOME=/app \
    UV_CACHE_DIR=/tmp/uv-cache

USER app
EXPOSE 8000

# `uv run --no-sync` executes inside the project env WITHOUT re-resolving
# dependencies at boot (the image is already synced and frozen).
CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
