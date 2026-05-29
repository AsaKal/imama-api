from fastapi import APIRouter
from db.database import SessionLocal
from services.pregnancy_services import get_user_pregnancy_data

router = APIRouter()

@router.get("/pregnancy-data/{user_id}")
def pregnancy_data(user_id: int):
    db = SessionLocal()
    return get_user_pregnancy_data(db, user_id)
