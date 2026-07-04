import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.system import router as system_router
from app.services.chat_service import chat_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    chat_service.load_model()
    yield
    chat_service.unload_model()


app = FastAPI(
    title="IMaMa API",
    description="Maternal health chatbot API powered by a local HuggingFace model",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(system_router)
app.include_router(chat_router)
