from typing import Dict, Any, Optional
from pydantic import BaseModel
from typing_extensions import List

class ClassifierRequest(BaseModel):
    features: Dict[str, Any]

class ClassifierResponse(BaseModel):
    prediction: int
    proba: float
    model_version: str
    latency_ms: float
    artifact_source: str
    event_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str = 'ok'

class MetricsResponse(BaseModel):
    total_predictions: int
    churn_rate: float
    avg_latency_ms: Optional[float] = None

class LLMRequest(BaseModel):
    query: str

class LLMResponse(BaseModel):
    answer: str
    sources: List[str]
    llm_tier: str
    latency_ms: float
    model_provider: str
    embedding_model: str
    context_tokens_estimate: int
