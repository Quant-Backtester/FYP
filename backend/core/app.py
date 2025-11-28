#External
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


#Custom
from auth import auth_router
from middlewares import LoggingMiddleware
from configs import settings


def create_app() -> FastAPI:
    """ the main function that create the server """
    app = FastAPI(title="Trading Backend")
    

    
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.allowed_origin,
        allow_credentials=True,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
    )
    
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch= LoggingMiddleware())
    
    #TODO add this in production system
    # app.add_middleware(HTTPSRedirectMiddleware)
    
    app.include_router(router=auth_router)

    
    return app