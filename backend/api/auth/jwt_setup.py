# STL
from datetime import datetime, timedelta, timezone

# external
import jwt
from configs import settings

# custom
from custom.custom_type import JwtToken, VerificationToken
from custom.custom_enums import PayloadEnum
from configs import get_logger


logger = get_logger()

def create_access_token(data: JwtToken) -> str:
  to_encode = JwtToken(
    sub=data["sub"],
    username=data["username"],
    email=data["email"],
    exp=datetime.now() + timedelta(minutes=settings.access_token_expire_minutes),
  )
  return jwt.encode(
    payload=to_encode,  # type: ignore
    key=settings.jwt_secret_key,
    algorithm=settings.algorithm,
  )


def create_verification_token(email: str, username: str) -> str:
  """Create a short-lived token for email verification."""
  expire: datetime = datetime.now(timezone.utc) + timedelta(hours=settings.verify_token_expire_hour)

  payload = VerificationToken(username=username, email=email, exp=expire, what=PayloadEnum.VERIFICATION)

  return jwt.encode(
    payload=payload, # type: ignore
    key=settings.jwt_secret_key,
    algorithm=settings.algorithm,
  )


def verify_verification_token(token: str) -> str | None:
  """Return email if valid, None otherwise."""
  payload = jwt.decode(
    jwt=token, key=settings.jwt_secret_key, algorithms=[settings.algorithm]
  )
  logger.info(payload)
  if payload.get("what") != PayloadEnum.VERIFICATION:
    return None
  return payload.get("sub")


__all__ = ()
