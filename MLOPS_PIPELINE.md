# MLOps Pipeline

The ASFOTEC stack uses a reproducible MLflow-based workflow to train, evaluate, and promote the churn classifier. All entrypoints live under `mlops/` and can be orchestrated end to end with `mlops/run_all.py`.

## Lifecycle Stages

1. **Data ingestion & cleaning** – `mlops/training/feature_pipeline.py` loads `data/telco_churn.csv`, handles categorical encoding, trains the preprocessor, and persists it as an MLflow artifact.
2. **Model training** – `mlops/training/train_classifier.py` fits a LightGBM classifier using the features above, logs metrics (AUC, accuracy, F1), registers the model, and tags the run with the Git SHA for traceability.
3. **Offline evaluation** – `mlops/eval_classifier.py` reloads the freshly trained model, scores a hold-out set, and compares the metrics to the last *Production* model.
4. **Quality gate + promotion** – `mlops/quality_gate.py` enforces metric thresholds and, when passed, transitions the candidate to the `Production` stage. The FastAPI service always serves the latest `Production` tag.
5. **Batch execution** – `mlops/run_all.py` stitches the previous scripts together, making it easy to retrain locally or via CI.

## Running the Pipeline

### One-shot execution

```bash
poetry run python mlops/run_all.py \
  --experiment-name asfotec-churn \
  --register-name churn-classifier
```

This command expects the following environment variables (set them in `.env` or export before running):

- `MLFLOW_TRACKING_URI=http://localhost:5000` (or your remote server)
- `MLFLOW_S3_ENDPOINT_URL=http://localhost:9000`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (MinIO credentials)

### Stage-by-stage commands

```bash
# Build/update feature artifacts
poetry run python mlops/training/feature_pipeline.py

# Train & register a new model version
poetry run python mlops/training/train_classifier.py

# Evaluate the newly trained model against hold-out data
poetry run python mlops/eval_classifier.py

# Apply production quality gate & promote
poetry run python mlops/quality_gate.py --min-auc 0.82 --min-accuracy 0.78
```

All scripts log to MLflow, so you can inspect metrics/params via the MLflow UI (served by the Docker compose file on port `5000`).

## Artifacts & Registry

- **Preprocessor + model** – stored in the MLflow artifact store (MinIO bucket `mlflow`).
- **Registered model** – `churn-classifier`. `ModelService` queries this registry at API startup to fetch the current `Production` version.
- **Feature importance & evaluation plots** – saved under the same run directory, making it easy to audit a version after promotion.

## Automation Hooks

- GitHub Actions or Azure DevOps agents can call the same scripts; they only need network access to MLflow + MinIO.
- The API container does not bundle training dependencies, keeping runtime slim; model refresh requires re-running the pipeline and letting MLflow / ModelService handle the rollout automatically.
