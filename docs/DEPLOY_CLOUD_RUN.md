# Deploying the API to Cloud Run

This guide walks through packaging the FastAPI service into a container, pushing it to Artifact Registry, and creating a Cloud Run service that connects back to external dependencies (MLflow, MinIO/S3, Kafka). Adjust names to match your GCP project.

> **Prerequisites**
> - gcloud CLI authenticated (`gcloud auth login` and `gcloud config set project <PROJECT_ID>`)
> - Artifact Registry repository (e.g., `us-central1-docker.pkg.dev/<PROJECT_ID>/asfotec/api`)
> - Access to MLflow + MinIO endpoints (reachable from Cloud Run via VPC connector or public ingress)
> - A persisted Chroma vector store directory (see "Ship the RAG store" below)

## 1. Build and Push the Image

```bash
REGION=us-central1
REPO=asfotec
IMAGE=api
PROJECT=<PROJECT_ID>
TAG=v1

# Build using the existing Dockerfile.api
pack_root=$(pwd)
docker build -f Dockerfile.api -t $REGION-docker.pkg.dev/$PROJECT/$REPO/$IMAGE:$TAG $pack_root

gcloud auth configure-docker $REGION-docker.pkg.dev

docker push $REGION-docker.pkg.dev/$PROJECT/$REPO/$IMAGE:$TAG
```

## 2. Provision Runtime Secrets

Use Secret Manager to store credentials referenced by the API:

```bash
gcloud secrets create mlflow-tracking-uri --data-file=- <<<"http://mlflow.internal:5000"
gcloud secrets create mlflow-s3-endpoint --data-file=- <<<"https://s3.yourdomain.com"
gcloud secrets create minio-access-key --data-file=- <<<"<AWS_ACCESS_KEY_ID>"
gcloud secrets create minio-secret-key --data-file=- <<<"<AWS_SECRET_ACCESS_KEY>"
gcloud secrets create google-api-key --data-file=- <<<"<only if LLM_PROVIDER=google>"
```

During deployment you will reference the latest versions of these secrets.

## 3. Ship the RAG Vector Store

The RAG service expects `chroma_db/` to exist inside the container.

Options:

1. **Bake into image (recommended for read-only KB)**
   - Run `poetry run python rag/ingest.py --docs-path rag/docs --vector-store chroma_db` locally.
   - Ensure the generated `chroma_db/` directory is included when building the Docker image (the Dockerfile already copies `rag/`).
2. **Load from Cloud Storage**
   - Store the Chroma files in a GCS bucket.
   - Add a startup script (entrypoint wrapper) that downloads the archive before launching Uvicorn.

If you plan to refresh documentation frequently, prefer option 2 and trigger ingestion in a CI job.

## 4. Deploy to Cloud Run

```bash
SERVICE=asfotec-api
VPC_CONNECTOR=<optional-shared-vpc-connector>
SUBNET=default

ENV_VARS="APP_NAME=ASFOTEC API,ENV=prod,LOG_LEVEL=INFO,LLM_PROVIDER=sherlock,MLFLOW_EXPERIMENT_NAME=asfotec-churn,MLFLOW_MODEL_NAME=churn-classifier,RAG_DOCS_PATH=rag/docs,RAG_VECTORSTORE_PATH=chroma_db"

gcloud run deploy $SERVICE \
  --image $REGION-docker.pkg.dev/$PROJECT/$REPO/$IMAGE:$TAG \
  --region $REGION \
  --platform managed \
  --port 8080 \
  --allow-unauthenticated \
  --set-env-vars $ENV_VARS \
  --set-secrets MLFLOW_TRACKING_URI=mlflow-tracking-uri:latest,MLFLOW_S3_ENDPOINT_URL=mlflow-s3-endpoint:latest,AWS_ACCESS_KEY_ID=minio-access-key:latest,AWS_SECRET_ACCESS_KEY=minio-secret-key:latest,GOOGLE_API_KEY=google-api-key:latest \
  --cpu 1 \
  --memory 1Gi \
  --min-instances 0 \
  --max-instances 5 \
  ${VPC_CONNECTOR:+--vpc-connector $VPC_CONNECTOR}
```

Notes:
- Remove `--allow-unauthenticated` if you prefer IAM-based access.
- If MLflow/MinIO/Kafka live in a private network, configure a Serverless VPC Access connector and firewall rules accordingly.
- Kafka connectivity often requires private IP reachability; if not available, consider deploying the API alongside Kafka within the same VPC (e.g., GKE or Compute Engine) or leverage a managed pub/sub bridge.

## 5. Health Checks & Monitoring

- Cloud Run uses HTTP health probes on `/` by default. Add a custom probe hitting `/health` via `--service-account` + load balancer or configure gRPC health checks if fronted by API Gateway.
- Stream logs to Cloud Logging automatically; filter by `jsonPayload.message` to investigate inference errors.
- Expose metrics by scraping `/metrics/overview` or forwarding prediction events from Kafka into Cloud Monitoring.

## 6. Updating the Service

1. Rebuild image (or roll out a new tag after running the training + ingestion pipelines).
2. `docker push ...` new tag.
3. `gcloud run deploy ... --image ...:new-tag` (other flags optional).
4. Verify the URL returned by gcloud with curl.

## 7. Troubleshooting

- **CrashLoop / 503** – inspect `gcloud run services logs read $SERVICE` for stack traces; ensure env vars and secrets are present.
- **Model not found** – confirm MLflow registry is reachable and the credentials have `s3:ListBucket` + `GetObject` permissions on the artifacts bucket.
- **RAG store missing** – check that `chroma_db/` exists inside the container (`docker run --rm IMAGE ls chroma_db`). If mounting from GCS, validate the startup script path.
