# ASFOTEC-MLStack — Projet livré en 4h
## Full MLOps + RAG + API + MLflow + Kafka + New Gen UI — production-grade demo

Ce repository démontre ce qui peut être livré en 4 heures réelles, en suivant une méthodologie structurée :

- **30 minutes** — Élaboration PRD et architecture cible
- **1 heure** — Setup environnement IA + contexte Codex GPT-5.1
- **2 heures** — Génération Argentic IA + correction + architecture MLOps/RAG
- **30 minutes** — Intégration finale + stabilisation infra Docker + UI Polish

**Le résultat :**
Une stack d’entreprise complète, modulaire, stable, documentée, exploitable en production.

<img width="1920" height="919" alt="ASFOTEC MLStack Control- localhost" src="https://github.com/user-attachments/assets/1dffa1c5-86e4-45f0-923e-7b3844c0365d" />

---

## 🚀 1. Fonctionnalités principales

### ✔ MLOps complet (training → eval → quality gate → MLflow Registry)
- **Training LightGBM**
- **Auto-évaluation**
- **Quality Gate configurable**
- **MLflow Tracking + Artifacts**
- **MinIO comme S3 store**
- **Fallback automatique** si MLflow est down

### ✔ FastAPI production-ready
Endpoints exposés :

| Route | Description |
|-------|-------------|
| `GET /health` | Health check |
| `POST /predict/classifier` | ML tabulaire (LightGBM) |
| `POST /predict/llm` | RAG + LLM (mock provider) |
| `GET /metrics/overview` | Stats logs/Postgres |
| `GET /meta/architecture` | Architecture interne JSON |

### ✔ RAG (Retrieval-Augmented Generation)
- **Embeddings MiniLM**
- **Stockage vectoriel :** Chroma
- **Sources stockées** dans `rag/docs/*`
- **Retour complet :** answer + sources + latency + tier

### ✔ Kafka intégré pour audit ML
- chaque prédiction → **Kafka Producer**
- design prêt pour **Kafka Consumer** → Postgres

### ✔ Interface Utilisateur (UI) - New Gen
Une interface moderne et réactive pour piloter la stack :
- **Framework :** Next.js 14 (App Router)
- **Design System :** Tailwind CSS + Variables CSS (Shadcn/UI style)
- **Composants :** Radix UI primitives (Dialog, Slot, etc.)
- **Visualisation :** Recharts (Graphiques temps réel), Mermaid (Diagrammes d'architecture)
- **State Management :** TanStack Query (React Query)
- **Icons :** Lucide React

### ✔ Docker Compose complet
Services :
- FastAPI
- MLflow
- Kafka + Zookeeper
- MinIO
- Postgres
- UI (preview)

**Un seul script suffit :**
```bash
bash asfotec_init.sh
```

---

## 📦 2. Structure du projet

```
ASFOTEC-MLStack
├── apps/
│   ├── api/             # API FastAPI complète
│   └── ui/              # Dashboard UI (Next.js/Tailwind)
├── docs/                # Documentation complète
│   ├── ARCHITECTURE.md
│   ├── MLOPS_PIPELINE.md
│   ├── TRAINING_PIPELINE.md
│   ├── API_REFERENCE.md
│   ├── RAG_DESIGN.md
│   ├── DEPLOY_CLOUD_RUN.md
│   └── LOCAL_DEV_GUIDE.md
├── mlops/               # Training pipeline
│   ├── training/
│   ├── eval/
│   ├── quality_gate.py
│   └── run_all.py
├── rag/                 # RAG engine + docs
├── infra/docker/        # Stack Docker complète
├── scripts/             # Kafka consumer & outils
├── Makefile             # Commandes rapides
└── asfotec_init.sh      # Script orchestration complet
```

---

## ⚙️ 3. Installation rapide

### A. Installer dépendances
```bash
poetry install
cp .env.example .env
```

### B. Lancer stack Docker
```bash
make up
```

### C. Tester API
```bash
curl http://localhost:8000/health
```

### D. Lancer interface UI
```bash
cd apps/ui
npm install
npm run preview
```
*L'UI sera accessible sur http://localhost:4000*

---

## 🧪 4. Exemples de requêtes

### Classifier
```bash
curl -X POST http://localhost:8000/predict/classifier \
  -H "Content-Type: application/json" \
  -d '{"features":{"tenure":12,"MonthlyCharges":70}}'
```

### RAG
```bash
curl -X POST http://localhost:8000/predict/llm \
  -H "Content-Type: application/json" \
  -d '{"query":"Explique l architecture ASFOTEC-MLStack"}'
```

**Résultat :**
```json
{
 "answer": "...",
 "sources": [...],
 "llm_tier": "mock-local",
 "latency_ms": 77.74
}
```

---

## 📈 5. Pourquoi ce projet impressionne

- **livré en 4h** avec specs professionnelles
- **architecture complète et cohérente**
- **très proche d’une mise en prod réelle**
- **entièrement modulaire**
- **lisible et éducatif**
- **robuste et démonstratif**
- **idéal pour entretien / portfolio / consulting**

C’est une preuve directe de capacité E2E :
**MLOps + Backend + RAG + Docker + Kafka + UI + MLflow** dans un temps contraint.

---

## 🌐 6. Déploiement futur (GCP Cloud Run)

Le projet est déjà prêt pour :
- déploiement stateless API
- stockage artefacts externe
- Cloud SQL + PubSub
- CI/CD GitHub Actions
- Terraform IaC

Consultez `docs/DEPLOY_CLOUD_RUN.md` pour plus de détails.

---

## 📄 7. Licence
MIT.

---

## 🙌 8. Contact
**ASFOTEC — Make IT Simple**
