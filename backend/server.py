
#External
from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel

#Custom
from core import settings
from core import create_app
from database import engine

if __name__ == "__main__":
    """ starting the server here """
    SQLModel.metadata.create_all(bind=engine)
    app: FastAPI = create_app()
    uvicorn.run(app=app, host=settings.host, port=settings.port)

    #run python server.py