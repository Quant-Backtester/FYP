from typing import Generator
from sqlmodel import create_engine, Session

from configs import settings

engine = create_engine(
  url=settings.database_url, echo=True, connect_args={"check_same_thread": False}
)


def get_session() -> Generator[Session, None, None]:
  """FastAPI dependency for auto-commit/rollback"""
  with Session(bind=engine) as session:
    try:
      yield session
      session.commit()
    except Exception:
      session.rollback()
      raise


__all__ = ("get_session", "engine")
