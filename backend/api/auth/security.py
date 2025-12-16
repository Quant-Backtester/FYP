# External
import bcrypt
from fastapi import HTTPException, status
from configs import settings
from sqlalchemy.orm import Session


# Custom
from database.models import User
from database.sql_statement import get_user_by_email


# Protected method
def _verify_password(plain_password: str, hashed_password: str) -> bool:
  """Verify a plain password against a hashed one"""
  return bcrypt.checkpw(
    password=plain_password.encode(encoding="utf-8"),
    hashed_password=hashed_password.encode(encoding="utf-8"),
  )

# Public Method
def generate_verify_url(host_prefix: str, token: str) -> str:
  verify_url: str = (
    f"http://{settings.host}:{settings.port}{host_prefix}/verify-email?token={token}"
  )
  return verify_url


def hash_password(password: str) -> str:
  """Hash a password"""
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password=password.encode(encoding="utf-8"), salt=salt)
  return hashed.decode(encoding="utf-8")


def authenticate_user(session: Session, username: str, password: str) -> User:
  """logic for login a user"""
  user = get_user_by_email(session=session, email=username)
  if not user or not _verify_password(
    plain_password=password, hashed_password=user.hashed_password
  ):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Not found",

    )
  return user

__all__ = ()