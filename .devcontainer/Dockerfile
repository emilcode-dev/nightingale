FROM python:3.11-slim-trixie AS base
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/
LABEL maintainer="emilcode-dev"

ENV UV_LINK_MODE=copy

# Additional dev tooling (e.g. Git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspaces

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# ---- Development image ----
FROM base AS dev

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        tree \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Install all dependencies (including dev/test/docs)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Default entrypoint — start bash
ENTRYPOINT ["/bin/bash"]