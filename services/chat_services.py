import uuid

from db.models import Conversation, Message
from services.ai_services import generate_response
from services.pregnancy_services import get_user_pregnancy_data
from db.database import SessionLocal


def handle_chat(user_id: int, message: str):
    db = SessionLocal()

    conversation = (
        db.query(Conversation)
        .filter(Conversation.user_id == str(user_id))
        .order_by(Conversation.created_at.desc())
        .first()
    )
    if not conversation:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=str(user_id),
            title="Chat",
        )
        db.add(conversation)
        db.commit()

    #Save user message
    user_msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation.id,
        content=message,
        role="user",
    )
    db.add(user_msg)
    db.commit()

    #Get recent messages
    history = (
        db.query(Message)
        .join(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Message.created_at.desc())
        .limit(10)
        .all()
    )

    #Build previous conversations for context
    previous_conversations = [
    {
        "message": chat.content,
        "sender": chat.role,
        "timestamp": chat.created_at.isoformat()
    }
    for chat in history
]
    #Get pregnancy context
    pregnancy_data = get_user_pregnancy_data(db, user_id)

    #Generate AI response
    ai_reply = generate_response(
        message=message,
        history=history,
        pregnancy_data=pregnancy_data
    )
    
    
    

    #Save AI response
    bot_msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation.id,
        content=ai_reply,
        role="assistant",
    )
    db.add(bot_msg)
    db.commit()
    db.close()

    return ai_reply
    
