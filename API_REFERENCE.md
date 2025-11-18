# API Reference

Base URL (local): `http://localhost:8000`

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/health` | Liveness probe used by Docker/Kubernetes. |
| POST | `/predict/classifier` | Scores Telco churn using the latest Production LightGBM model. |
| POST | `/predict/llm` | Answers free-form ops questions via the RAG/LLM stack. |
| GET | `/metrics/overview` | Returns in-memory aggregates for latency + success counts. |
| GET | `/meta/architecture` | Emits the runtime architecture summary, including dependencies. |

## `GET /health`

**Response** `200 OK`

```json
{"status": "ok"}
```

## `POST /predict/classifier`

**Request body**

```json
{
  "features": {
    "contract": "Month-to-month",
    "tenure": 17,
    "monthly_charges": 79.2,
    "internet_service": "Fiber optic",
    "tech_support": "No"
  }
}
```

**Success response** `200 OK`

```json
{
  "prediction": 1,
  "proba": 0.8123,
  "model_version": "churn-classifier:12",
  "latency_ms": 23.7
}
```

**Errors** – Validation errors return `422`. Runtime issues (e.g., missing model) return `500` with `{ "detail": "reason" }`.

## `POST /predict/llm`

**Request body**

```json
{
  "query": "How do I retrain the classifier?"
}
```

**Success response** `200 OK`

```json
{
  "answer": "Run mlops/run_all.py to rebuild the LightGBM model...",
  "sources": ["rag/docs/project_architecture.md#training"],
  "llm_tier": "mock-local",
  "latency_ms": 58.1
}
```

The `llm_tier` reflects whether the mock engine (`mock-local`) or Google Gemini (`google-flash`) served the response. Any upstream exception becomes a `500` with a descriptive `detail` string.

## `GET /metrics/overview`

Returns rolling latency and success counts gathered since process start.

```json
{
  "classifier": {
    "count": 128,
    "avg_latency_ms": 24.3,
    "success_rate": 0.984
  },
  "llm": {
    "count": 42,
    "avg_latency_ms": 87.1,
    "success_rate": 0.952
  }
}
```

## `GET /meta/architecture`

Useful for observability dashboards or to confirm environment configuration.

```json
{
  "app": {
    "name": "ASFOTEC API",
    "environment": "dev",
    "log_level": "INFO",
    "port": 8000
  },
  "services": [
    {"name": "api", "tech": "FastAPI", "endpoints": ["health", "predict/classifier", "predict/llm", "metrics/overview", "meta/architecture"]},
    {"name": "postgres", "port": 5432, "purpose": "metrics + logging"},
    {"name": "kafka", "bootstrap_servers": "kafka:9092", "purpose": "stream predictions"},
    {"name": "mlflow", "tracking_uri": "http://mlflow:5000", "purpose": "model registry + artifacts"},
    {"name": "minio", "ports": [9000, 9001], "purpose": "S3-compatible artifact store"}
  ],
  "models": {
    "classifier": {
      "type": "tabular churn",
      "framework": "LightGBM",
      "mlflow_experiment": "asfotec-churn",
      "stage": "Production"
    },
    "rag_llm": {
      "provider": "sherlock",
      "embedding_model": "all-MiniLM-L6-v2",
      "vector_store_path": "chroma_db",
      "docs_path": "rag/docs"
    }
  },
  "dependencies": {
    "mlflow": "http://mlflow:5000",
    "postgres_dsn": "postgresql://postgres:postgres@postgres:5432/postgres",
    "kafka": "kafka:9092"
  }
}
```
