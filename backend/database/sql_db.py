from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from configs import settings

engine = create_engine(
  url=settings.database_url, echo=settings.debug, connect_args={"check_same_thread": False}
)

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


__all__ = ("get_session", "engine")
