# External
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


# Custom
from api.auth import auth_router
from middlewares import LoggingMiddleware
from configs import settings
from custom.custom_handler import app_error_handler
from custom.custom_exception import AppError


def register_middleawre(app: FastAPI) -> None:
  app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.allowed_origin,
    allow_credentials=True,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
  )

  app.add_middleware(middleware_class=LoggingMiddleware)

  # app.add_middleware(HTTPSRedirectMiddleware)

  # add more middleware here


def register_routes(app: FastAPI) -> None:
  app.include_router(router=auth_router)


def register_exception_handler(app: FastAPI) -> None:
  app.add_exception_handler(
    exc_class_or_status_code=AppError, handler=app_error_handler # type: ignore
  )


def create_app() -> FastAPI:
  """the main function that create the server"""
  app = FastAPI(title="Trading Backend")

  register_middleawre(app=app)
  register_exception_handler(app=app)
  register_routes(app=app)

  return app


__all__ = ("create_app",)
