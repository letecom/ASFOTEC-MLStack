<<<<<<< HEAD
ASFOTEC-MLStack
Production-Ready MLOps & RAG Architecture
ASFOTEC-MLStack is a comprehensive, modular, and scalable Machine Learning infrastructure designed to demonstrate a full end-to-end enterprise lifecycle. It unifies traditional MLOps (Tabular), Generative AI (RAG), Real-time Streaming (Kafka), and a modern Observability Dashboard into a single, deployable stack.

<img width="1920" height="919" alt="ASFOTEC MLStack Control- localhost" src="https://github.com/user-attachments/assets/37830195-e527-4383-a08a-4dd5698c2b0d" />


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

=======
<div align="center">

# 🚀 ASFOTEC-MLStack

### Production-Ready MLOps & RAG Architecture

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A comprehensive, modular, and scalable Machine Learning infrastructure demonstrating full end-to-end enterprise lifecycle*

[Features](#-key-features) • [Architecture](#-architecture-overview) • [Quick Start](#-getting-started) • [API Docs](#-api-reference) • [Deployment](#️-deployment--cloud-run)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#-architecture-overview)
- [Technical Stack](#-technical-stack)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Deployment](#️-deployment--cloud-run)
- [Contact](#-contact)

---

## Overview

**ASFOTEC-MLStack** unifies traditional **MLOps** (Tabular), **Generative AI** (RAG), **Real-time Streaming** (Kafka), and a modern **Observability Dashboard** into a single, deployable stack.

![ASFOTEC MLStack Control](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

---

## 🏗 Architecture Overview

This project implements a robust **microservices architecture** orchestrated via Docker Compose, featuring:

- **MLOps Pipeline**: Automated training, evaluation, and quality gating for LightGBM models using MLflow
- **RAG Engine**: Vector search using ChromaDB and SentenceTransformers for context-aware LLM responses
- **Event Streaming**: Apache Kafka integration for prediction logging, auditing, and decoupled data processing
- **API Gateway**: High-performance FastAPI backend exposing model inference and metrics
- **Next-Gen UI**: A reactive Next.js 14 dashboard for real-time monitoring, latency tracking, and system health checks

---

## 🚀 Technical Stack

### Backend & AI

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI (Python) |
| **ML Framework** | LightGBM (Tabular), LangChain/Custom (RAG) |
| **Experiment Tracking** | MLflow (Registry & Artifacts) |
| **Vector Store** | ChromaDB |
| **Storage** | MinIO (S3 compatible object storage) |
| **Streaming** | Apache Kafka + Zookeeper |

### Frontend & Dashboard

| Component | Technology |
|-----------|-----------|
| **Framework** | Next.js 14 (App Router) |
| **Styling** | Tailwind CSS + Shadcn/UI |
| **Visualization** | Recharts (Real-time latency & throughput graphs) |
| **State Management** | TanStack Query |

---

## ⚡ Key Features

### 🎯 Complete MLOps Lifecycle

Automated pipeline handling tabular data (Churn Prediction):

- ✅ **Training**: LightGBM implementation
- ✅ **Auto-Evaluation**: Metrics calculation (Accuracy, F1, AUC)
- ✅ **Quality Gate**: Strict thresholds before model promotion to "Production"
- ✅ **Registry**: Full artifact versioning in MLflow with automatic fallback mechanisms

### 🧠 Retrieval-Augmented Generation (RAG)

A specialized subsystem for document intelligence:

- 🔍 **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- 📚 **Ingestion**: PDF/Doc indexing stored in `rag/docs/`
- 💬 **Inference**: Returns Answer + Source Context + Latency metrics + Tier status

### 📊 Real-Time Observability

The UI provides a "Control Tower" view:

- 💚 **Health Checks**: Live status of API Gateway
- 📈 **Latency Trends**: P95 and Average latency tracking for both Classifier and LLM endpoints
- 🔥 **Kafka Throughput**: Visualization of message volume and error rates
- 🎯 **Model Snapshots**: JSON view of currently loaded models and RAG configurations

### 🔄 Kafka Audit Trails

Every prediction request is asynchronously produced to a Kafka topic, enabling:

- 📝 Decoupled logging
- 🗄️ Future integration with data lakes (Postgres/BigQuery)
- 🔍 Real-time drift detection replay

---

## 📦 Project Structure

```bash
ASFOTEC-MLStack
├── apps
│   ├── api/             # FastAPI Gateway & Business Logic
│   └── ui/              # Next.js Dashboard & Visualization
├── infra
│   └── docker/          # Docker Compose & Configs (Kafka, MLflow, MinIO)
├── mlops
│   ├── training/        # Model training scripts
│   ├── eval/            # Evaluation & Metric computation
│   └── quality_gate.py  # Production promotion logic
├── rag/                 # RAG Engine, Vector Store & Documents
├── docs/                # Architecture & Deployment documentation
└── scripts/             # Utility scripts (Kafka consumers, Init)
```

---

## 🛠 Getting Started

### Prerequisites

- ✅ Docker & Docker Compose
- ✅ Python 3.10+ (for local dev)
- ✅ Node.js 18+ (for UI dev)

### 🚀 Initialization

The project includes a unified orchestrator script to set up the environment, spin up containers, and initialize the ML pipeline.

```bash
# Clone the repo
git clone https://github.com/letecom/ASFOTEC-MLStack.git

# Install dependencies & Init environment
bash asfotec_init.sh
```

### 🐳 Manual Docker Launch

If you prefer manual control:

```bash
>>>>>>> 49a3b68 (Upgrade README.md with GitHub-flair formatting)
make up
3. Accessing the Services
Dashboard UI: http://localhost:4000

<<<<<<< HEAD
API Documentation (Swagger): http://localhost:8000/docs

MLflow UI: http://localhost:5000
=======
### 🌐 Accessing the Services

| Service | URL |
|---------|-----|
| **Dashboard UI** | http://localhost:4000 |
| **API Documentation (Swagger)** | http://localhost:8000/docs |
| **MLflow UI** | http://localhost:5000 |
>>>>>>> 49a3b68 (Upgrade README.md with GitHub-flair formatting)

🔌 API Reference
The stack exposes RESTful endpoints for immediate inference:

<<<<<<< HEAD
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
=======
## 🔌 API Reference

The stack exposes RESTful endpoints for immediate inference:

### 📊 Tabular Prediction (Classifier)

```bash
curl -X POST http://localhost:8000/predict/classifier \
  -H "Content-Type: application/json" \
  -d '{"features":{"tenure":12, "MonthlyCharges":70.5, "TotalCharges": 850}}'
```

### 🧠 RAG Query (LLM)

```bash
curl -X POST http://localhost:8000/predict/llm \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain the MLOps lifecycle defined in the docs"}'
```

> 💡 Response includes grounded answers and source citations.
>>>>>>> 49a3b68 (Upgrade README.md with GitHub-flair formatting)

Stateless API: Ready for Google Cloud Run or AWS Fargate.

<<<<<<< HEAD
External State: Configurable to connect to managed services (RDS for DB, Confluent for Kafka, S3 for Artifacts).

CI/CD: GitHub Actions workflows compatible.

See docs/DEPLOY_CLOUD_RUN.md for production configuration.

🙌 Contact
ASFOTEC — Make IT Simple
=======
## ☁️ Deployment & Cloud Run

This stack is designed to be **cloud-agnostic**:

- ✅ **Stateless API**: Ready for Google Cloud Run or AWS Fargate
- ✅ **External State**: Configurable to connect to managed services (RDS for DB, Confluent for Kafka, S3 for Artifacts)
- ✅ **CI/CD**: GitHub Actions workflows compatible

📖 See [`docs/DEPLOY_CLOUD_RUN.md`](docs/DEPLOY_CLOUD_RUN.md) for production configuration.

---

## 🙌 Contact

**ASFOTEC — Make IT Simple**

---

<div align="center">

Made with ❤️ by the ASFOTEC Team

[⬆ Back to Top](#-asfotec-mlstack)

</div>
>>>>>>> 49a3b68 (Upgrade README.md with GitHub-flair formatting)
