

from fastapi import FastAPI
import uvicorn
import yaml

from core import create_app

if __name__ == "__main__":
    app: FastAPI = create_app()
    with open("settings.yaml") as f:
        config = yaml.safe_load(f)
    HOST = config["server"]["host"]
    PORT = config["server"]["port"]
    uvicorn.run(app=app, host=HOST, port=PORT)