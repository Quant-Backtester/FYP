# STL
from datetime import datetime, timedelta

# external
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from configs import settings

# custom
from custom.custom_type import JwtToken, VerificationToken
from custom.custom_enums import PayloadEnum
from custom.custom_exception import TokenError, TokenExpiredError
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
  expire: datetime = datetime.now() + timedelta(hours=settings.verify_token_expire_hour)

  payload = VerificationToken(
    sub=username, email=email, exp=expire, what=PayloadEnum.VERIFICATION
  )

  return jwt.encode(
    payload=payload,  # type: ignore
    key=settings.jwt_secret_key,
    algorithm=settings.algorithm,
  )


def verify_verification_token(token: str) -> str:
  try:
    payload = jwt.decode(
      jwt=token,
      key=settings.jwt_secret_key,
      algorithms=[settings.algorithm],
      options={"require": ["sub"]},
    )
  except ExpiredSignatureError as e:
    raise TokenExpiredError(message="Verification token expired") from e
  except InvalidTokenError as e:
    raise TokenError(message="Invalid verification token") from e

  email = payload.get("sub")

  if not isinstance(email, str) or not email:
    raise TokenError(message="Invalid verification token")

  return email


__all__ = ()
