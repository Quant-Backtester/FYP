from typing import Any, Generator
from sqlmodel import create_engine, Session

from core import settings

engine = create_engine(settings.database_url, echo=True, connect_args={"check_same_thread": False})

def get_session() -> Generator[Session, Any, None]:
    """use this to get the database session """
    with Session(engine) as session:
        yield session

__all__ = [
    "engine", 
    "get_session",
]