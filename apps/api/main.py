import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.settings import get_settings
from .routers.classifier import router as classifier_router
from .routers.llm import router as llm_router
from .routers.meta import router as meta_router
from .routers.metrics import router as metrics_router
from .schemas import HealthResponse

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description='ML/LLM/MLOps demo per PRD',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(classifier_router)
app.include_router(llm_router)
app.include_router(metrics_router)
app.include_router(meta_router)

@app.get('/health', response_model=HealthResponse)
async def health():
    return HealthResponse()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=settings.port)
