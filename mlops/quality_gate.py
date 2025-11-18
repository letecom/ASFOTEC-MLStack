import sys
from typing import Dict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mlflow

from mlops.utils import resolve_tracking_uri, apply_mlflow_env

THRESHOLDS = {'test_accuracy': 0.90, 'test_f1': 0.88}


def enforce_quality(settings, metrics: Dict[str, float], run_id: str) -> None:
    """Validate metrics against thresholds and tag Production if ok."""

    apply_mlflow_env(settings)
    tracking_uri = resolve_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)
    client = mlflow.tracking.MlflowClient(tracking_uri=tracking_uri)

    for key, threshold in THRESHOLDS.items():
        value = metrics.get(key)
        if value is None or value < threshold:
            raise ValueError(f'Quality gate failed for {key}: {value} < {threshold}')

    client.set_tag(run_id, 'stage', 'Production')


if __name__ == '__main__':
    from mlops.config import get_settings
    import json
    from pathlib import Path

    metrics = json.loads((Path('mlops/artifacts/eval_report.json')).read_text())
    run_id = metrics['run_id']
    enforce_quality(get_settings(), metrics, run_id)
    print('Quality gate passed and Production tag applied.')
