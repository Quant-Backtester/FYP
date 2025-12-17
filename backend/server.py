# External
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Custom
from database.sql_db import Base
from configs import settings, setup_logging
from database.sql_db import engine
from middlewares import LoggingMiddleware
from api.auth import auth_router
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



if __name__ == "__main__":
  """ starting the server here """
  setup_logging()

  Base.metadata.create_all(bind=engine)
  app: FastAPI = create_app()
  uvicorn.run(app=app, host=settings.host, port=settings.port)

  # run python server.py
