# Training Pipeline Playbook

This guide explains how the ASFOTEC churn model is prepared, evaluated, and promoted with the utilities under `mlops/`. It is intended for ML engineers who need to retrain locally or wire the steps into CI/CD jobs.

## Dataset & Features

- **Source**: `data/telco_churn.csv` (structured customer account fields).
- **Targets**: Binary `churn` label recorded as `Yes/No`.
- **Feature handling**:
  - Categorical columns (contract type, payment method, internet service, etc.) are one-hot encoded via `sklearn` pipelines.
  - Numerical features (tenure, charges) are standardized to zero mean / unit variance.
  - Columns used by the pipeline are defined inside `mlops/training/feature_pipeline.py` for a single source of truth.

## Pipeline Stages

| Stage | Script | Responsibilities |
| ----- | ------ | ---------------- |
| Feature engineering | `mlops/training/feature_pipeline.py` | Load CSV, split train/validation, build preprocessing pipeline, log artifacts to MLflow. |
| Model training | `mlops/training/train_classifier.py` | Fit LightGBM classifier, log metrics (AUC, accuracy, F1), register new version. |
| Post-training evaluation | `mlops/eval_classifier.py` | Reload candidate model, score hold-out set, compare vs. last Production metrics. |
| Quality gate & promotion | `mlops/quality_gate.py` | Apply thresholds (configurable flags) and transition the model to `Production` when successful. |
| Orchestration | `mlops/run_all.py` | Runs the full chain with consistent arguments; ideal for CI or local refresh. |

## Required Environment Variables

Before running any script, export the values below or store them in `.env` (loaded via `python-dotenv`).

| Variable | Purpose |
| -------- | ------- |
| `MLFLOW_TRACKING_URI` | Address of the MLflow tracking server (e.g., `http://localhost:5000`). |
| `MLFLOW_S3_ENDPOINT_URL` | MinIO/S3 endpoint storing artifacts. |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Credentials for the artifact store. |
| `MLFLOW_EXPERIMENT_NAME` | Defaults to `asfotec-churn`; overrides allowed. |
| `MLFLOW_MODEL_NAME` | Registered model name; default `churn-classifier`. |

Set them quickly with:

```bash
export $(grep -v '^#' .env | xargs)
```

## Running Locally

### Full orchestration

```bash
poetry run python mlops/run_all.py \
  --experiment-name asfotec-churn \
  --register-name churn-classifier \
  --min-auc 0.82 \
  --min-accuracy 0.78
```

What happens:
1. Feature artifacts logged (transformers, column metadata).
2. LightGBM is trained and logged as a new MLflow run.
3. Evaluation script checks drift/regression.
4. Quality gate promotes the run to `Production` once thresholds pass.

### Individual debugging

- `poetry run python mlops/training/feature_pipeline.py --test-split 0.2`
- `poetry run python mlops/training/train_classifier.py --num-leaves 64 --learning-rate 0.05`
- `poetry run python mlops/eval_classifier.py --baseline-stage Production`

Each script prints the MLflow run ID so you can inspect artifacts via the UI.

## CI/CD Integration Tips

1. **Cache dependencies** – the scripts rely on Poetry-managed environments; install with `poetry install --with mlops` if you define extras.
2. **Remote MLflow** – point `MLFLOW_TRACKING_URI` to a reachable server (self-hosted MLflow behind VPN or Databricks-compatible endpoint).
3. **Artifact store** – when running in CI, set `MLFLOW_S3_ENDPOINT_URL` to MinIO’s internal address (e.g., `http://minio:9000`) and provision the same credentials as the Docker stack.
4. **Promotion approvals** – wrap `mlops/quality_gate.py` inside a manual approval stage if required. You can run it with `--dry-run` to report metrics without changing stages.
5. **Notifications** – the scripts return non-zero status codes on failure, making it easy to trigger Slack/email alerts.

## Deliverables

After success, you should see:

- A new `Production` model version in MLflow (`Models > churn-classifier`).
- Logged artifacts: preprocessing pipeline, LightGBM booster, feature importances PNG, evaluation metrics JSON.
- Kafka-ready metadata embedded in the model (tags include `git_sha` and timestamp). The FastAPI `ModelService` fetches the latest `Production` version automatically on restart.
