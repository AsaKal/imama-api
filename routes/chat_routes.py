from fastapi import APIRouter
from services.chat_services import handle_chat

router = APIRouter()

@router.post("/chat")
def chat(user_id: int, message: str):
    response = handle_chat(user_id, message)
    return {"reply": response}

