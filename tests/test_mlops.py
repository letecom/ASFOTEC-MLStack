import pytest
import subprocess
import os
from pathlib import Path

def test_pipeline():
    os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'  # Mock
    result = subprocess.run(['python', 'mlops/run_all.py'], capture_output=True)
    assert result.returncode == 0, 'Pipeline must pass quality gate'
    
    report = Path('mlops/artifacts/eval_report.json').read_text()
    metrics = eval(report)  # Simple
    assert metrics['test_f1'] >= 0.88
    assert metrics['test_accuracy'] >= 0.90
