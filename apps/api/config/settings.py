"""Centralized application settings leveraging Pydantic BaseSettings.

All components import `get_settings()` to guarantee a single cached
configuration source backed by environment variables/.env files.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application wide configuration loaded from env/.env."""

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local'),
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False,
    )

    # Core
    app_name: str = Field(default='ASFOTEC-MLStack-Demo API', alias='APP_NAME')
    env: str = Field(default='dev', alias='ENV')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')

    # API
    port: int = Field(default=8080, alias='PORT')

    # Database
    postgres_host: str = Field(default='postgres', alias='POSTGRES_HOST')
    postgres_port: int = Field(default=5432, alias='POSTGRES_PORT')
    postgres_db: str = Field(default='predictions_log', alias='POSTGRES_DB')
    postgres_user: str = Field(default='postgres', alias='POSTGRES_USER')
    postgres_password: str = Field(default='postgres', alias='POSTGRES_PASSWORD')
    postgres_dsn: Optional[str] = Field(default=None, alias='POSTGRES_DSN')

    # MLflow / MLOps
    mlflow_tracking_uri: str = Field(default='http://localhost:5000', alias='MLFLOW_TRACKING_URI')
    mlflow_experiment_name: str = Field(default='ChurnClassifier', alias='MLFLOW_EXPERIMENT_NAME')
    mlflow_registry_uri: Optional[str] = Field(default=None, alias='MLFLOW_REGISTRY_URI')
    mlflow_artifact_uri: Optional[str] = Field(default=None, alias='MLFLOW_ARTIFACT_URI')
    mlflow_artifact_bucket: Optional[str] = Field(default=None, alias='MLFLOW_ARTIFACT_BUCKET')
    mlflow_s3_endpoint_url: Optional[str] = Field(default=None, alias='MLFLOW_S3_ENDPOINT_URL')
    aws_access_key_id: Optional[str] = Field(default=None, alias='AWS_ACCESS_KEY_ID')
    aws_secret_access_key: Optional[str] = Field(default=None, alias='AWS_SECRET_ACCESS_KEY')

    # Kafka
    kafka_bootstrap_servers: Optional[str] = Field(default=None, alias='KAFKA_BOOTSTRAP_SERVERS')
    kafka_topic_predictions: str = Field(default='predictions', alias='KAFKA_TOPIC_PREDICTIONS')

    # RAG / LLM
    rag_docs_path: Path = Field(default=Path('rag/docs'), alias='RAG_DOCS_PATH')
    rag_vectorstore_path: Path = Field(default=Path('chroma_db'), alias='RAG_VECTORSTORE_PATH')
    rag_top_k: int = Field(default=3, alias='RAG_TOP_K')
    embedding_model_name: str = Field(
        default='sentence-transformers/all-MiniLM-L6-v2',
        alias='EMBEDDING_MODEL_NAME',
    )
    llm_provider: Literal['sherlock', 'google'] = Field(default='sherlock', alias='LLM_PROVIDER')
    google_api_key: Optional[str] = Field(default=None, alias='GOOGLE_API_KEY')

    @property
    def resolved_postgres_dsn(self) -> str:
        if self.postgres_dsn:
            return self.postgres_dsn
        return (
            f'postgresql://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Singleton accessor so settings stay consistent across imports."""

    return AppSettings()
