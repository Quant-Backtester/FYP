#External
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Custom
from auth import auth_router

def create_app() -> FastAPI:
    """ the main function that create the server """
    app = FastAPI(title="Trading Backend")
    
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth_router)

    
    return app