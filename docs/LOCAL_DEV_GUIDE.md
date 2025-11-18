# Local Development Guide

Follow these steps to run the ASFOTEC ML/LLM stack end to end on a single workstation.

## 1. Prerequisites

- Docker + Docker Compose v2
- Python 3.10 and Poetry (`pip install poetry`)
- At least 8 GB RAM available for the containers

## 2. Repository Setup

```bash
git clone <repo-url>
cd ASFOTEC-MLStack-Demo
poetry install
cp .env.example .env  # edit credentials as needed
```

Key environment variables (all defined in `.env.example`):

- `MLFLOW_TRACKING_URI`, `MLFLOW_S3_ENDPOINT_URL` – point to the MLflow + MinIO services from Docker.
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` – MinIO credentials (match docker-compose).
- `LLM_PROVIDER` – `sherlock` (mock) or `google`.
- `GOOGLE_API_KEY` – required only when `LLM_PROVIDER=google`.

## 3. Start the Infrastructure

```bash
docker compose -f infra/docker/docker-compose.dev.yml up -d
```

This launches Postgres, Kafka/ZooKeeper, MinIO, MLflow, and the API container (with the repo mounted so code edits reflect immediately). Inspect logs via `docker compose ... logs -f api` as needed.

## 4. Train & Promote the Classifier

Run the full pipeline to ensure a `Production` model exists:

```bash
poetry run python mlops/run_all.py \
  --experiment-name asfotec-churn \
  --register-name churn-classifier
```

The run logs metrics to MLflow (browse `http://localhost:5000`). Once promoted, the API automatically reloads the newest `Production` version.

## 5. Build the RAG Vector Store

```bash
poetry run python rag/ingest.py \
  --docs-path rag/docs \
  --vector-store chroma_db
```

The command splits Markdown files, generates embeddings, and saves them into `chroma_db/`, which the API container mounts for retrieval.

## 6. Smoke Test the API

```bash
curl -s http://localhost:8000/health

curl -s -X POST http://localhost:8000/predict/classifier \
  -H "Content-Type: application/json" \
  -d '{"features": {"contract": "Month-to-month", "tenure": 10}}'

curl -s -X POST http://localhost:8000/predict/llm \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I retrain the classifier?"}'
```

You should see valid JSON responses plus latency/model metadata.

## 7. Run the Test Suite

```bash
poetry run pytest
```

Tests cover the FastAPI routers (`tests/test_api.py`) and MLOps helpers (`tests/test_mlops.py`). Add new cases alongside feature work.

## 8. Tear Down

```bash
docker compose -f infra/docker/docker-compose.dev.yml down -v
```

Removing volumes ensures MinIO/Kafka state is rebuilt next time. Keep `chroma_db/` if you want to persist the ingested documentation between runs.
