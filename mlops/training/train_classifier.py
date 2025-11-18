import json
from pathlib import Path
from typing import Dict, Tuple
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import lightgbm as lgb
import mlflow
import mlflow.lightgbm
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

from mlops.config import AppSettings
from mlops.utils import resolve_tracking_uri, apply_mlflow_env, ensure_mlflow_artifact_bucket
from .feature_pipeline import preprocess_pipeline, load_and_split_data


def train_model(settings: AppSettings) -> Tuple[str, Dict[str, float]]:
    """Train churn classifier, log to MLflow, and return (run_id, metrics)."""

    apply_mlflow_env(settings)
    ensure_mlflow_artifact_bucket(settings)
    tracking_uri = resolve_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    with mlflow.start_run(run_name='ChurnClassifier-Auto') as run:
        X_train, X_test, y_train, y_test = load_and_split_data()

        preprocessor = preprocess_pipeline()
        X_train_proc = preprocessor.fit_transform(X_train)
        X_test_proc = preprocessor.transform(X_test)

        mlflow.log_param('n_features', X_train_proc.shape[1])
        mlflow.log_param('train_size', len(X_train))
        mlflow.log_param('test_size', len(X_test))

        params = {
            'n_estimators': 200,
            'learning_rate': 0.05,
            'max_depth': -1,
            'random_state': 42,
            'subsample': 0.9,
            'colsample_bytree': 0.9,
        }
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train_proc, y_train)

        y_train_pred = model.predict(X_train_proc)
        y_test_pred = model.predict(X_test_proc)

        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_f1 = f1_score(y_test, y_test_pred)

        metrics = {
            'train_accuracy': float(train_acc),
            'test_accuracy': float(test_acc),
            'test_f1': float(test_f1),
        }

        mlflow.log_params(params)
        for key, value in metrics.items():
            mlflow.log_metric(key, value)

        joblib.dump(preprocessor, 'preprocessor.joblib')
        mlflow.log_artifact('preprocessor.joblib')

        feature_names = preprocessor.get_feature_names_out()
        feature_importance = pd.DataFrame(
            {'feature': feature_names, 'importance': model.feature_importances_}
        ).sort_values('importance', ascending=False)
        feature_importance.to_csv('feature_importance.csv', index=False)
        mlflow.log_artifact('feature_importance.csv')

        schema = {
            'numerical_features': list(preprocessor.transformers_[0][2]),
            'categorical_features': list(preprocessor.transformers_[1][2]),
        }
        Path('feature_schema.json').write_text(json.dumps(schema, indent=2))
        mlflow.log_artifact('feature_schema.json')

        X_train.head(20).to_csv('training_sample.csv', index=False)
        mlflow.log_artifact('training_sample.csv')

        mlflow.lightgbm.log_model(model, 'model')

        return run.info.run_id, metrics


if __name__ == '__main__':
    from mlops.config import get_settings

    run_id, metrics = train_model(get_settings())
    print(f'Train complete. Run: {run_id}, metrics: {metrics}')
