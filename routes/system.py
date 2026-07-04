from fastapi import APIRouter

from app.services.chat_service import chat_service

router = APIRouter(tags=["system"])


@router.get("/")
def root():
    return {"name": "IMaMa API", "docs": "/docs", "health": "/health"}


@router.get("/health")
def health():
    return {"status": "ok", "model_loaded": chat_service.model_loaded}
