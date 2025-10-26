FROM python:3.11-slim AS base
LABEL maintainer="emilcode-dev"

# Set working directory
WORKDIR /app

# Additional dev tooling (e.g. Git, etc.)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#         ffmpeg \
#         && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip

# Install requirements
COPY requirements_prod.txt .
RUN pip install --no-cache-dir -r requirements_prod.txt
# # python production requirements
# RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
#     pip install --requirement /tmp/requirements.txt

COPY . .

RUN pip install --no-cache-dir .

# Ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1
ENV DATABRICKS_TOKEN= ...
ENV DATABRICKS_HOST=https://....cloud.databricks.com
ENV MLFLOW_TRACKING_URI=databricks
ENV MLFLOW_REGISTRY_URI=databricks-uc
ENV MLFLOW_EXPERIMENT_ID=...


EXPOSE 8080

CMD ["uvicorn", "app.fastapi.main:app", "--host", "0.0.0.0", "--port", "8080"]
