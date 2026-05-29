from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_services import handle_chat

router = APIRouter()
class ChatRequest(BaseModel):
    user_id: int
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    return {"reply": handle_chat(req.user_id, req.message)}

