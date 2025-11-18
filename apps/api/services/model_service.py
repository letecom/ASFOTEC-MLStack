import json
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib
import pandas as pd
from confluent_kafka import Producer
import mlflow.lightgbm
from mlflow.tracking import MlflowClient

from apps.api.config.settings import get_settings
from mlops.utils import resolve_tracking_uri, apply_mlflow_env

class ModelService:
    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger(self.__class__.__name__)
        apply_mlflow_env(self.settings)
        self._initialized = False
        self.model = None
        self.preprocessor = None
        self.feature_names_in_ = None
        self.version = None
        self._artifact_source = 'unknown'
        self.artifact_dir = Path('/tmp/model_artifacts')
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        self.tracking_uri = resolve_tracking_uri(
            self.settings.mlflow_tracking_uri,
            allow_fallback=False,
            logger=self.logger,
        )
        self._artifact_source = (
            'mlflow-remote'
            if self.tracking_uri.startswith(('http://', 'https://'))
            else 'mlflow-local'
        )
        self.client = MlflowClient(tracking_uri=self.tracking_uri)
        self.producer = self._init_producer()

    def _init_producer(self):
        bootstrap_servers = self.settings.kafka_bootstrap_servers
        if not bootstrap_servers:
            return None
        return Producer({'bootstrap.servers': bootstrap_servers})

    def _load_model(self):
        if self._initialized:
            return
        exp_name = self.settings.mlflow_experiment_name
        exp = self.client.get_experiment_by_name(exp_name)
        if not exp:
            raise RuntimeError(f'Experiment {exp_name} not found on MLflow server {self.tracking_uri}')
        
        runs = self.client.search_runs(
            experiment_ids=[exp.experiment_id],
            filter_string="tags.stage = 'Production'",
            order_by=['start_time DESC'],
            max_results=1
        )
        if not runs:
            raise RuntimeError('No Production stage model found. Run MLOps pipeline and promote a model first.')
        
        run_id = runs[0].info.run_id
        self.version = run_id
        
        self.logger.info('Loading Production model %s from %s', run_id, self.tracking_uri)

        preprocessor_path = self.client.download_artifacts(
            run_id, 'preprocessor.joblib', str(self.artifact_dir)
        )
        self.preprocessor = joblib.load(preprocessor_path)
        self.feature_names_in_ = self.preprocessor.feature_names_in_
        
        model_uri = f'runs:/{run_id}/model'
        self.model = mlflow.lightgbm.load_model(model_uri)
        
        self._initialized = True
        self.logger.info('Loaded Production model %s', run_id)

    def _prepare_features(self, features: Dict[str, Any]) -> pd.DataFrame:
        df = pd.DataFrame([features])
        expected = list(self.feature_names_in_)
        missing = [col for col in expected if col not in df.columns]
        if missing:
            raise ValueError(f'Missing required features: {missing}')
        df = df[expected]
        return df

    def predict(self, features: Dict[str, Any]) -> Tuple[int, float, float, Optional[str]]:
        self._load_model()
        start_time = time.time()

        df = self._prepare_features(features)
        X_proc = self.preprocessor.transform(df)

        prediction = int(self.model.predict(X_proc)[0])
        proba = float(self.model.predict_proba(X_proc)[0][1])
        latency_ms = (time.time() - start_time) * 1000
        event_id = str(uuid.uuid4())

        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'prediction': prediction,
            'proba': proba,
            'model_version': self.version,
            'latency_ms': latency_ms,
            'features': features,
            'event_id': event_id,
        }
        if self.producer:
            try:
                self.producer.produce('predictions', key=event_id, value=json.dumps(event))
                self.producer.flush()
            except Exception as exc:
                self.logger.warning('Failed to publish prediction event: %s', exc)

        return prediction, proba, latency_ms, event_id if self.producer else None

    def get_version(self) -> str:
        self._load_model()
        return self.version

    @property
    def artifact_source(self) -> str:
        return self._artifact_source

from functools import lru_cache

@lru_cache()
def get_model_service() -> ModelService:
    service = ModelService()
    # Pre-load model on startup to avoid first-request latency
    try:
        service._load_model()
    except Exception as e:
        service.logger.warning(f"Could not pre-load model: {e}")
    return service
