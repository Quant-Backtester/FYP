from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel


from core import settings
from app import create_app
from database import engine

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    app: FastAPI = create_app()
    uvicorn.run(app=app, host=settings.host, port=settings.port)