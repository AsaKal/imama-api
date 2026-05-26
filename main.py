from fastapi import FastAPI
from db import models  # noqa: F401
from db.database import engine, Base

app = FastAPI()
# print("Hello World")

Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")

@app.get("/")
def home():
    return {"message": "DB initialized successfully"}
