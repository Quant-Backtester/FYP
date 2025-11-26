#External
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Custom
from auth import auth_router

def create_app() -> FastAPI:
    """ the main function that create the server """
    app = FastAPI(title="Trading Backend")
    
    origin = [
        "http://localhost:5173",
    ]
    allow_methods = [
        "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"
    ]
    
    allow_headers = [
        "*"
    ]
    
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=origin,
        allow_credentials=True,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )
    
    app.include_router(auth_router)

    
    return app