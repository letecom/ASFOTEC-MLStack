# ASFOTEC MLStack Architecture

This document captures the relationships between the FastAPI service, the MLOps toolchain, and the supporting infrastructure. All components are deployable through `infra/docker/docker-compose.dev.yml` for local development.

## Stack Overview

- **FastAPI application (`apps/api`)** – exposes `/predict/classifier`, `/predict/llm`, `/metrics/overview`, `/meta/architecture`, and `/health`.
- **Model Service** – loads the latest MLflow *Production* model, performs LightGBM inference, and publishes prediction events to Kafka.
- **RAG / LLM Orchestrator** – retrieves chunks from a persistent Chroma vector store, optionally enriches answers with Google Gemini, and returns `answer + sources + tier + latency`.
- **Postgres** – stores prediction metrics when Kafka consumers are enabled; also backs the `/metrics/overview` API in production (the dev build exposes in-memory metrics).
- **Kafka** – captures prediction events for asynchronous processing and analytics.
- **MLflow + MinIO** – MLflow tracks experiments/metrics while MinIO provides the S3-compatible artifact store that backs the registry.
- **Chroma vector store (`chroma_db/`)** – holds embeddings for the RAG workflow and is mounted into the API container for persistence.

## Textual Diagram

```
[HTTP Client]
      |
      v
+-------------------+
|   FastAPI (api)   |
+-------------------+
| Routers:          |
| - /health         |
| - /predict/*      |
| - /metrics        |
| - /meta           |
+-------------------+
  |            |
  |            |
  v            v
ModelService   LLMOrchestrator
  |                |
  |                v
  |         RAGService -> Chroma (embeddings)
  v
MLflow Tracking -> MinIO (artifacts)
  |
  v
Kafka -> (future consumer) -> Postgres metrics store
```

## Classifier Request Flow

1. **Client call** hits `POST /predict/classifier` with structured Telco features.
2. **ModelService** lazy-loads the latest MLflow run tagged `Production` (via `mlops/quality_gate.py`).
3. **Preprocessor + LightGBM model** (stored as MLflow artifacts) transform features and score churn probability.
4. **Kafka event** (topic `predictions`) is emitted with latency, features, version, and probabilities.
5. **HTTP response** returns `{prediction, proba, model_version, latency_ms}` while metrics are fed to the in-memory `MetricsCollector`.

## RAG / LLM Flow

1. **Client call** hits `POST /predict/llm` with a free-form query.
2. **LLMOrchestrator** delegates retrieval to `rag/service.py`, which loads the Chroma vector store from `chroma_db/`.
3. **RAGService** retrieves the top-`k` chunks, formats a lightweight context, and:
   - uses a mock deterministic answer if `LLM_PROVIDER=sherlock` (default), or
   - calls Google Gemini via LangChain when `LLM_PROVIDER=google` plus `GOOGLE_API_KEY`.
4. **Response** includes the generated answer, the list of source documents, the tier (`mock-local` or `google-flash`), and observed latency.

## Observability & Configuration

- Settings are centralized in `apps/api/config/settings.py` (Pydantic BaseSettings) and load values from `.env` or Docker overrides.
- `mlops/utils.py` enforces that MLflow and MinIO credentials are available to both host and container processes.
- `/meta/architecture` returns a machine-readable snapshot describing the deployed components, making it easy to verify the live topology.
- `/metrics/overview` surfaces rolling latency/success counts through the in-memory `MetricsCollector`. A production Kafka consumer can persist the same events to Postgres for historical reporting.
