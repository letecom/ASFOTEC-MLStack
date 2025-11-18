# Architecture Projet (from PRD §4)

[Client HTTP]
 ↓
[FastAPI]
├─ /predict/classifier → ModelService → MLflow Prod
│  └→ Kafka Producer → Kafka → Consumer → Postgres
├─ /predict/llm → LLMOrchestrator → LangChain + RAG (Chroma)
├─ /meta/architecture → RAG query
└─ /metrics/overview → Postgres query

MLOps: train → eval → quality_gate → register
CI/CD: GHA → Docker → Artifact Reg → Cloud Run
Infra: Terraform GCP
