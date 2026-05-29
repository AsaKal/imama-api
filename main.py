from fastapi import FastAPI
from db import models
from db.database import engine, Base
from routes.chat_routes import router as chat_router
from routes.pregnancy_routes import router as pregnancy_router
from routes.auth_routes import router as auth_router
from routes.ai_routes import router as ai_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "DB initialized successfully"}

app.include_router(chat_router)
app.include_router(pregnancy_router)
app.include_router(auth_router)
app.include_router(ai_router)
