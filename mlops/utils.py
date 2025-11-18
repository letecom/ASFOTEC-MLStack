"""Utility helpers for MLOps scripts."""

import logging
import os
from pathlib import Path
import sys
from typing import Optional, TYPE_CHECKING
from urllib.parse import urljoin, urlparse

import boto3
from botocore.exceptions import ClientError
import requests

if TYPE_CHECKING:  # pragma: no cover - imported only for typing
    from apps.api.config.settings import AppSettings


def ensure_project_root_on_path() -> None:
    """Ensure repo root is on sys.path when running scripts directly."""
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def resolve_tracking_uri(
    preferred_uri: str,
    fallback_subdir: str = 'mlops/mlruns',
    *,
    allow_fallback: bool = True,
    logger: Optional[logging.Logger] = None,
) -> str:
    """Return a usable MLflow tracking URI, optionally falling back to a local file store."""

    if not preferred_uri.lower().startswith('http'):
        return preferred_uri

    if _is_mlflow_available(preferred_uri):
        return preferred_uri

    message = f'MLflow server at {preferred_uri} unreachable.'

    if not allow_fallback:
        if logger:
            logger.error(message)
        else:
            print(f'❌ {message}')
        raise ConnectionError(message)

    fallback_path = (Path(__file__).resolve().parents[1] / fallback_subdir).resolve()
    fallback_path.mkdir(parents=True, exist_ok=True)
    fallback_uri = f'file:{fallback_path}'
    notice = f"⚠️  {message} Falling back to local store {fallback_uri}."
    if logger:
        logger.warning(notice)
    else:
        print(notice)
    return fallback_uri


def _is_mlflow_available(base_url: str, timeout: float = 2.0) -> bool:
    """Ping the MLflow REST endpoint to confirm it is reachable."""

    base = base_url.rstrip('/') + '/'
    health_url = urljoin(base, 'health')
    if _check_endpoint(health_url, timeout=timeout):
        return True
    # Fallback to legacy experiments endpoint if /health is unavailable
    experiments_url = urljoin(base, 'api/2.0/mlflow/experiments/list')
    return _check_endpoint(experiments_url, method='get', timeout=timeout)


def _check_endpoint(url: str, method: str = 'get', timeout: float = 2.0) -> bool:
    try:
        response = requests.request(method=method.lower(), url=url, timeout=timeout)
        return response.ok
    except requests.RequestException:
        return False


def apply_mlflow_env(settings: 'AppSettings') -> None:
    """Surface MLflow/MinIO credentials to os.environ for MLflow/boto3 clients."""

    env_map = {
        'MLFLOW_S3_ENDPOINT_URL': getattr(settings, 'mlflow_s3_endpoint_url', None),
        'MLFLOW_ARTIFACT_URI': getattr(settings, 'mlflow_artifact_uri', None),
        'AWS_ACCESS_KEY_ID': getattr(settings, 'aws_access_key_id', None),
        'AWS_SECRET_ACCESS_KEY': getattr(settings, 'aws_secret_access_key', None),
    }

    for key, value in env_map.items():
        if value and not os.environ.get(key):
            os.environ[key] = value


def ensure_mlflow_artifact_bucket(settings: 'AppSettings') -> None:
    """Create the configured artifact bucket on MinIO if it does not exist."""

    bucket = _resolve_bucket_name(settings)
    if not bucket:
        return

    endpoint = getattr(settings, 'mlflow_s3_endpoint_url', None)
    access_key = getattr(settings, 'aws_access_key_id', None)
    secret_key = getattr(settings, 'aws_secret_access_key', None)

    if not all([endpoint, access_key, secret_key]):
        return

    client = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    try:
        client.head_bucket(Bucket=bucket)
    except ClientError as exc:
        error_code = exc.response.get('Error', {}).get('Code')
        if error_code in {'404', 'NoSuchBucket'}:
            client.create_bucket(Bucket=bucket)
        else:
            raise


def _resolve_bucket_name(settings: 'AppSettings') -> Optional[str]:
    if getattr(settings, 'mlflow_artifact_bucket', None):
        return settings.mlflow_artifact_bucket
    artifact_uri = getattr(settings, 'mlflow_artifact_uri', None)
    if artifact_uri:
        parsed = urlparse(artifact_uri)
        if parsed.scheme == 's3' and parsed.netloc:
            return parsed.netloc
    return None
