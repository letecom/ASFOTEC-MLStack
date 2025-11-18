import json
from pathlib import Path
from typing import Dict, Tuple
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import mlflow
import mlflow.lightgbm
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, roc_auc_score

from mlops.config import AppSettings
from mlops.utils import resolve_tracking_uri, apply_mlflow_env
from mlops.training.feature_pipeline import load_and_split_data

ARTIFACTS_DIR = Path('mlops/artifacts')
ARTIFACTS_DIR.mkdir(exist_ok=True)


def evaluate_run(settings: AppSettings, run_id: str) -> Tuple[Dict[str, float], Path]:
    """Evaluate a specific MLflow run and persist eval_report.json."""

    apply_mlflow_env(settings)
    tracking_uri = resolve_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)
    client = mlflow.tracking.MlflowClient(tracking_uri=tracking_uri)

    X_train, X_test, y_train, y_test = load_and_split_data()

    preprocessor_path = client.download_artifacts(run_id, 'preprocessor.joblib', str(ARTIFACTS_DIR))
    preprocessor = joblib.load(preprocessor_path)

    model_uri = f'runs:/{run_id}/model'
    model = mlflow.lightgbm.load_model(model_uri)

    X_test_proc = preprocessor.transform(X_test)
    y_pred = model.predict(X_test_proc)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, model.predict_proba(X_test_proc)[:, 1])
    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        'run_id': run_id,
        'test_accuracy': float(acc),
        'test_f1': float(f1),
        'test_auc': float(auc),
        'confusion_matrix': cm,
    }

    report_path = ARTIFACTS_DIR / 'eval_report.json'
    report_path.write_text(json.dumps(metrics, indent=2))

    client.log_artifact(run_id, str(report_path))

    return metrics, report_path


if __name__ == '__main__':
    from mlops.config import get_settings
    from mlflow.tracking import MlflowClient

    settings = get_settings()
    tracking_uri = resolve_tracking_uri(settings.mlflow_tracking_uri)
    client = MlflowClient(tracking_uri=tracking_uri)
    exp = client.get_experiment_by_name(settings.mlflow_experiment_name)
    run = client.search_runs([exp.experiment_id], order_by=['start_time DESC'], max_results=1)[0]
    metrics, path = evaluate_run(settings, run.info.run_id)
    print(f'Evaluation metrics: {metrics}')
    print(f'Report saved to {path}')
