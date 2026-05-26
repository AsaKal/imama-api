from fastapi import FastAPI
from pydantic import BaseModel
from db.models import Conversation, User, Message, Appointment, Attachment, Embedding
from db.database import SessionLocal

app = FastAPI()

@app.post("/bot")
def generate_response(message, context):
    #Get user prompt and context
    prompt = build_prompt(message, context)
    response = call_llm(prompt)
    return response

def build_prompt(message, context):
    #Build prompt for LLM using message and context
    prompt = f"User message: {message}\nContext: {context}\nResponse:"
    return prompt

def call_llm(prompt):
    #Call LLM API with prompt and return response
    #This is a placeholder for actual LLM integration
    response = "This is a generated response based on the prompt."
    return response

def save_conversation(user_id, message, sender):
    db = SessionLocal()
    conversation = Conversation(user_id=user_id, message=message, sender=sender)
    db.add(conversation)
    db.commit()
    db.close()
    
def save_message(user_id, message, sender):
    db = SessionLocal()
    msg = Message(user_id=user_id, message=message, sender=sender)
    db.add(msg)
    db.commit()
    db.close()