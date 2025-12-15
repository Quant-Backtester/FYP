# STL

# external
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

# Custom
from database.sql_db import Base


class User(Base):
  __tablename__ = "user"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
  hashed_password: Mapped[str] = mapped_column(String(255))
  is_verified: Mapped[bool] = mapped_column(Boolean, default=False)


__all__ = ("User", )