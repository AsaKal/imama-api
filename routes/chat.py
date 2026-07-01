from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


# ------------------------------------------------------------------ #
# Schemas
# ------------------------------------------------------------------ #

class NewConversationRequest(BaseModel):
    user_id: str = Field(..., description="Unique ID of the user starting a conversation", examples=["user-1"])


class ConversationResponse(BaseModel):
    conversation_id: str


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Unique ID of the user sending the message", examples=["user-1"])
    conversation_id: str = Field(..., description="ID of an existing conversation, or a new one to start it", examples=["00000000-0000-0000-0000-000000000000"])
    message: str = Field(..., description="The message to send to Imama", examples=["Habari, nina wiki 22 za ujauzito na nina maumivu ya kichwa."])


class ChatResponse(BaseModel):
    user_id: str
    conversation_id: str
    response: str
    timestamp: str


# ------------------------------------------------------------------ #
# Conversation endpoints
# ------------------------------------------------------------------ #

@router.post("/conversation/new", response_model=ConversationResponse)
def new_conversation(req: NewConversationRequest):
    """Create a new conversation for a user and return its conversation_id."""
    conversation_id = chat_service.create_conversation(req.user_id)
    return ConversationResponse(conversation_id=conversation_id)


@router.delete("/conversation/{conversation_id}")
def end_conversation(conversation_id: str):
    """Delete a conversation and its history."""
    chat_service.delete_conversation(conversation_id)
    return {"status": "deleted", "conversation_id": conversation_id}


@router.get("/conversation/{conversation_id}/history")
def get_history(conversation_id: str):
    """Return the message history for a conversation."""
    conversation = chat_service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conversation_id, "history": conversation["history"]}


# ------------------------------------------------------------------ #
# Chat endpoint
# ------------------------------------------------------------------ #

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a message to Imama and receive a response.

    If the conversation_id does not exist, a new conversation is created
    automatically and owned by user_id.
    """
    try:
        response = chat_service.generate_response(
            req.conversation_id, req.user_id, req.message
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

    return ChatResponse(
        user_id=req.user_id,
        conversation_id=req.conversation_id,
        response=response,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ------------------------------------------------------------------ #
# Model status endpoint
# ------------------------------------------------------------------ #

@router.get("/status")
def model_status():
    """Check whether the HuggingFace model is loaded and ready."""
    return {
        "model_loaded": chat_service.model_loaded,
        "backend": "pytorch",
        "conversation_count": len(chat_service.conversations),
    }
