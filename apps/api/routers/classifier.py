import time
from fastapi import APIRouter, HTTPException, Depends
from ..schemas import ClassifierRequest, ClassifierResponse
from ..services.model_service import ModelService, get_model_service
from ..services.metrics_collector import metrics_collector

router = APIRouter(prefix='/predict', tags=['predict'])

@router.post('/classifier', response_model=ClassifierResponse)
async def predict_classifier(request: ClassifierRequest, service: ModelService = Depends(get_model_service)):
    start = time.time()
    try:
        prediction, proba, latency_ms, event_id = service.predict(request.features)
        metrics_collector.record('classifier', (time.time() - start) * 1000, success=True)
        return ClassifierResponse(
            prediction=prediction,
            proba=proba,
            model_version=service.version,
            latency_ms=latency_ms,
            artifact_source=service.artifact_source,
            event_id=event_id,
        )
    except Exception as e:
        metrics_collector.record('classifier', (time.time() - start) * 1000, success=False)
        raise HTTPException(status_code=500, detail=str(e))
