import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health():
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'

@pytest.mark.skip('Requires MLflow model')
def test_classifier():
    features = {'tenure': 12, 'MonthlyCharges': 50.0, 'TotalCharges': 600.0, 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes'}  # Minimal
    resp = client.post('/predict/classifier', json={'features': features})
    assert resp.status_code == 200  # Or 500 if no model
