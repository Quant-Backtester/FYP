# STL
from typing import Generator

# External
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session

# Custom
from configs import settings

url_object = URL.create(
  drivername=settings.database_driver,
  username=settings.database_username,
  password=settings.database_password,
  host=settings.database_host,
  database=settings.database,
  port=settings.database_port,
)

engine = create_engine(url=url_object)

sql_session = Session(bind=engine)


class Base(DeclarativeBase):
  pass


def get_session() -> Generator[Session, None, None]:
  """FastAPI dependency for auto-commit/rollback"""
  with sql_session as session:
    try:
      yield session
      session.commit()
    except Exception:
      session.rollback()
      raise
