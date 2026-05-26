from fastapi import FastAPI
from numpy import record
from pydantic import BaseModel
from db.models import Conversation, Message, User, Appointment, Attachment, Embedding
from services.ai_services import generate_response

app = FastAPI()

def get_user_pregnancy_data(db, user_id):
    # Example query to fetch pregnancy data (this is just a placeholder and should be adapted to your actual database schema)
    pregnancy_data = {
        "user_id": user_id,
        "current_week": record.current_week,
        "trimester": get_trimester(record.current_week),
        "symptoms": record.symptoms or [],
        "conversation_id": chats[0].id if chats else None,
        "previous_conversations": previous_conversations,
        "description": build_description(record)
        
        
    }
    # return pregnancy_data
    print(f"{user_id} (this is a placeholder function, implement actual data fetching logic)")

def get_trimester(week):
    if week <= 12:
        return "First Trimester"
    elif 13 <= week <= 26:
        return "Second Trimester"
    else:
        return "Third Trimester"
    
def build_description(record):
    description = f"User is currently in week {record.current_week} of pregnancy, which is in the {get_trimester(record.current_week)}. "
    if record.symptoms:
        description += f"User is experiencing the following symptoms: {', '.join(record.symptoms)}. "
    else:
        description += "No data available."
    return description

@app.get("/pregnancy-data/{user_id}")
def pregnancy_data(user_id: int):
    # Fetch pregnancy data for the user
    pregnancy_data = get_user_pregnancy_data(db, user_id)
    return pregnancy_data