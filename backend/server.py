

from fastapi import FastAPI
import uvicorn


from core import create_app, settings

if __name__ == "__main__":
    app: FastAPI = create_app()
    uvicorn.run(app=app, host=settings.host, port=settings.port)