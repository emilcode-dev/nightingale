FROM python:3.11-slim AS base
LABEL maintainer="emilcode-dev"

# Additional dev tooling (e.g. Git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        tree \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install Python dependencies
RUN pip install --upgrade pip

# CMD ["python", "main.py"]