# STL
from datetime import datetime, timedelta, timezone

# third party
import jwt
from configs import settings

# custom
from custom.custom_type import JwtToken


def create_access_token(data: JwtToken) -> str:
  to_encode = JwtToken(
    sub=data["sub"],
    email=data["email"],
    exp=datetime.now() + timedelta(minutes=settings.access_token_expire_minutes),
  )
  return jwt.encode(
    payload=to_encode,  # type: ignore
    key=settings.jwt_secret_key,
    algorithm=settings.algorithm,
  )


def create_verification_token(email: str) -> str:
  """Create a short-lived token for email verification."""
  expire = datetime.now(timezone.utc) + timedelta(minutes=30)

  return jwt.encode(
    payload={"sub": email, "exp": expire, "type": "verification"},
    key=settings.jwt_secret_key,
    algorithm=settings.algorithm,
  )


def verify_verification_token(token: str) -> str | None:
  """Return email if valid, None otherwise."""
  payload = jwt.decode(
    jwt=token, key=settings.jwt_secret_key, algorithms=[settings.algorithm]
  )
  if payload.get("type") != "verification":
    return None
  return payload.get("sub")


__all__ = ()
