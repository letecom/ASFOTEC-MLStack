import json
from pathlib import Path

from fastapi import APIRouter, Depends

from ..config.settings import AppSettings, get_settings

router = APIRouter(prefix='/meta', tags=['meta'])

ROOT = Path(__file__).resolve().parents[3]
FEATURE_SCHEMA_PATH = ROOT / 'feature_schema.json'
TRAIN_EVAL_SUMMARY_PATH = ROOT / 'mlops' / 'artifacts' / 'train_eval_summary.json'


def _load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


@router.get('/architecture')
async def get_architecture(settings: AppSettings = Depends(get_settings)):
    feature_schema = _load_json(FEATURE_SCHEMA_PATH)
    model_metrics = _load_json(TRAIN_EVAL_SUMMARY_PATH)
    artifact_source = (
        'mlflow-remote'
        if settings.mlflow_tracking_uri.startswith(('http://', 'https://'))
        else 'mlflow-local'
    )
    docs_path = settings.rag_docs_path
    docs_count = len(list(docs_path.rglob('*.md'))) if docs_path.exists() else 0
    vector_ready = settings.rag_vectorstore_path.exists()

    return {
        'app': {
            'name': settings.app_name,
            'environment': settings.env,
            'log_level': settings.log_level,
            'port': settings.port,
        },
        'services': [
            {'name': 'api', 'tech': 'FastAPI', 'endpoints': ['health', 'predict/classifier', 'predict/llm', 'metrics/overview', 'meta/architecture']},
            {'name': 'postgres', 'port': settings.postgres_port, 'purpose': 'metrics + logging'},
            {'name': 'kafka', 'bootstrap_servers': settings.kafka_bootstrap_servers, 'purpose': 'stream predictions'},
            {'name': 'mlflow', 'tracking_uri': settings.mlflow_tracking_uri, 'purpose': 'model registry + artifacts'},
            {'name': 'minio', 'ports': [9000, 9001], 'purpose': 'S3-compatible artifact store'},
        ],
        'models': {
            'classifier': {
                'type': 'tabular churn',
                'framework': 'LightGBM',
                'mlflow_experiment': settings.mlflow_experiment_name,
                'stage': 'Production',
                'artifact_source': artifact_source,
                'latest_metrics': model_metrics,
            },
            'rag_llm': {
                'provider': settings.llm_provider,
                'embedding_model': settings.embedding_model_name,
                'vector_store_path': str(settings.rag_vectorstore_path),
                'docs_path': str(settings.rag_docs_path),
                'docs_indexed': docs_count,
                'vectorstore_ready': vector_ready,
            },
        },
        'dependencies': {
            'mlflow': settings.mlflow_tracking_uri,
            'postgres_dsn': settings.resolved_postgres_dsn,
            'kafka': settings.kafka_bootstrap_servers,
        },
        'feature_schema': feature_schema,
    }
