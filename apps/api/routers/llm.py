import time

from fastapi import APIRouter, Depends, HTTPException

from ..schemas import LLMRequest, LLMResponse
from ..services.llm_orchestrator import LLMOrchestrator
from ..services.metrics_collector import metrics_collector

router = APIRouter(prefix='/predict', tags=['llm'])


@router.post('/llm', response_model=LLMResponse)
async def predict_llm(request: LLMRequest, service: LLMOrchestrator = Depends(LLMOrchestrator)):
    start = time.time()
    try:
        response = service.query(request.query)
        metrics_collector.record('llm', (time.time() - start) * 1000, success=True)
        return response
    except Exception as exc:  # noqa: BLE001 - we want to capture all errors for telemetry
        metrics_collector.record('llm', (time.time() - start) * 1000, success=False)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
