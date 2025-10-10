FROM python:3.11-slim AS base
LABEL maintainer="emilcode-dev"

# Poetry environment
# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="$POETRY_HOME/bin:$PATH"

# Additional dev tooling (e.g. Git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ffmpeg \
        && rm -rf /var/lib/apt/lists/*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /workspace

# Copy only dependency-related files first (for better build caching)
COPY ./poetry.lock ./pyproject.toml ./

# Install only runtime dependencies (without dev dependencies)
RUN poetry install --only main --no-root


# ---- Development image ----
FROM base AS dev

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        tree

# Install all dependencies (including dev/test/docs)
RUN poetry install --no-root

# Default entrypoint — start bash
ENTRYPOINT ["/bin/bash"]