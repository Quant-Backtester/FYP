from typing import Any, Generator
from sqlmodel import create_engine, Session

from core import settings

engine = create_engine(settings.database_url, echo=True, connect_args={"check_same_thread": False})

def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency for auto-commit/rollback"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

__all__ = (
    "engine", 
    "get_session",
)