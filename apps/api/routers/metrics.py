from fastapi import APIRouter, Depends

from ..services.metrics_service import MetricsService

router = APIRouter(prefix='/metrics', tags=['metrics'])


@router.get('/overview')
async def get_metrics_overview(service: MetricsService = Depends(MetricsService)):
    return service.get_overview()
