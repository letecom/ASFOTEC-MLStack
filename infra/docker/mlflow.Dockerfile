FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /mlflow

RUN pip install --no-cache-dir mlflow==3.6.0 boto3

EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "s3://mlflow-artifacts", "--host", "0.0.0.0", "--port", "5000", "--disable-security-middleware", "--no-serve-artifacts"]
