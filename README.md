ASFOTEC-MLStack
Production-Ready MLOps & RAG Architecture
ASFOTEC-MLStack is a comprehensive, modular, and scalable Machine Learning infrastructure designed to demonstrate a full end-to-end enterprise lifecycle. It unifies traditional MLOps (Tabular), Generative AI (RAG), Real-time Streaming (Kafka), and a modern Observability Dashboard into a single, deployable stack.

<img width="1920" height="919" alt="ASFOTEC MLStack Control- localhost" src="https://github.com/user-attachments/assets/95280555-4efd-418c-b6d6-3b0e70e3a027" />

🏗 Architecture Overview
This project implements a robust microservices architecture orchestrated via Docker Compose, featuring:

MLOps Pipeline: Automated training, evaluation, and quality gating for LightGBM models using MLflow.

RAG Engine: Vector search using ChromaDB and SentenceTransformers for context-aware LLM responses.

Event Streaming: Apache Kafka integration for prediction logging, auditing, and decoupled data processing.

API Gateway: High-performance FastAPI backend exposing model inference and metrics.

Next-Gen UI: A reactive Next.js 14 dashboard for real-time monitoring, latency tracking, and system health checks.

🚀 Technical Stack
Backend & AI
Framework: FastAPI (Python)

ML Framework: LightGBM (Tabular), LangChain/Custom (RAG)

Experiment Tracking: MLflow (Registry & Artifacts)

Vector Store: ChromaDB

Storage: MinIO (S3 compatible object storage)

Streaming: Apache Kafka + Zookeeper

Frontend & Dashboard
Framework: Next.js 14 (App Router)

Styling: Tailwind CSS + Shadcn/UI

Visualization: Recharts (Real-time latency & throughput graphs)

State Management: TanStack Query

⚡ Key Features
1. Complete MLOps Lifecycle
Automated pipeline handling tabular data (Churn Prediction):

Training: LightGBM implementation.

Auto-Evaluation: Metrics calculation (Accuracy, F1, AUC).

Quality Gate: Strict thresholds before model promotion to "Production".

Registry: Full artifact versioning in MLflow with automatic fallback mechanisms.

2. Retrieval-Augmented Generation (RAG)
A specialized subsystem for document intelligence:

Embeddings: sentence-transformers/all-MiniLM-L6-v2.

Ingestion: PDF/Doc indexing stored in rag/docs/.

Inference: Returns Answer + Source Context + Latency metrics + Tier status.

3. Real-Time Observability
The UI provides a "Control Tower" view (as seen in the screenshots):

Health Checks: Live status of API Gateway.

Latency Trends: P95 and Average latency tracking for both Classifier and LLM endpoints.

Kafka Throughput: Visualization of message volume and error rates.

Model Snapshots: JSON view of currently loaded models and RAG configurations.

4. Kafka Audit Trails
Every prediction request is asynchronously produced to a Kafka topic, enabling:

Decoupled logging.

Future integration with data lakes (Postgres/BigQuery).

Real-time drift detection replay.

📦 Project Structure
Bash

ASFOTEC-MLStack
├── apps
│   ├── api              # FastAPI Gateway & Business Logic
│   └── ui               # Next.js Dashboard & Visualization
├── infra
│   └── docker           # Docker Compose & Configs (Kafka, MLflow, MinIO)
├── mlops
│   ├── training         # Model training scripts
│   ├── eval             # Evaluation & Metric computation
│   └── quality_gate.py  # Production promotion logic
├── rag                  # RAG Engine, Vector Store & Documents
├── docs                 # Architecture & Deployment documentation
└── scripts              # Utility scripts (Kafka consumers, Init)
🛠 Getting Started
Prerequisites
Docker & Docker Compose

Python 3.10+ (for local dev)

Node.js 18+ (for UI dev)

1. Initialization
The project includes a unified orchestrator script to set up the environment, spin up containers, and initialize the ML pipeline.

Bash

# Clone the repo
git clone https://github.com/your-org/ASFOTEC-MLStack.git

# Install dependencies & Init environment
bash asfotec_init.sh
2. Manual Docker Launch
If you prefer manual control:

Bash

make up
3. Accessing the Services
Dashboard UI: http://localhost:4000

API Documentation (Swagger): http://localhost:8000/docs

MLflow UI: http://localhost:5000

🔌 API Reference
The stack exposes RESTful endpoints for immediate inference:

Tabular Prediction (Classifier)
Bash

curl -X POST http://localhost:8000/predict/classifier \
  -H "Content-Type: application/json" \
  -d '{"features":{"tenure":12, "MonthlyCharges":70.5, "TotalCharges": 850}}'
RAG Query (LLM)
Bash

curl -X POST http://localhost:8000/predict/llm \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain the MLOps lifecycle defined in the docs"}'
Response includes grounded answers and source citations.

☁️ Deployment & Cloud Run
This stack is designed to be cloud-agnostic.

Stateless API: Ready for Google Cloud Run or AWS Fargate.

External State: Configurable to connect to managed services (RDS for DB, Confluent for Kafka, S3 for Artifacts).

CI/CD: GitHub Actions workflows compatible.

See docs/DEPLOY_CLOUD_RUN.md for production configuration.

🙌 Contact
ASFOTEC — Make IT Simple
