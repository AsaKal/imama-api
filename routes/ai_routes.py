from fastapi import FastAPI, APIRouter
from services.ai_services import generate_response

router = APIRouter()

@router.post("/ai")
def ai_response(prompt: str):
    response = generate_response(prompt)
    return {"response": response}

