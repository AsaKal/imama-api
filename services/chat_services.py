from fastapi import FastAPI
from pydantic import BaseModel
from db.models import Conversation, Message, User
from services.ai_services import generate_response
from services.pregnancy_services import get_user_pregnancy_data
from db.database import SessionLocal

app = FastAPI()

# services/chat_service.py
@app.post("/chat")
def handle_chat(user_id: int, message: str):
    db = SessionLocal()

    # 1. Save user message
    user_chat = Conversation(user_id=user_id, message=message, sender="user")
    db.add(user_chat)
    db.commit()

    # 2. Get recent messages (memory)
    get_recent_messages = lambda db, user_id: db.query(Message).join(Conversation).filter(Conversation.user_id == user_id).order_by(Message.created_at.desc()).limit(10).all()
    history = get_recent_messages(db, user_id)

    # 3. Get pregnancy context
    pregnancy_data = get_user_pregnancy_data(db, user_id)

    # 4. Generate AI response
    ai_reply = generate_response(
        message=message,
        history=history,
        pregnancy_data=pregnancy_data
    )

    # 5. Save AI response
    bot_chat = Conversation(user_id=user_id, message=ai_reply, sender="bot")
    db.add(bot_chat)
    db.commit()

    return ai_reply