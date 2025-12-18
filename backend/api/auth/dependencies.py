# external
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Custom
from configs import settings
from common.exceptions import InvalidCredentialsError


async def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(dependency=HTTPBearer()),
):
  payload = jwt.decode(
    jwt=credentials.credentials,
    key=settings.jwt_secret_key,
    algorithms=[settings.algorithm],
  )
  user_id: str = payload.get("sub")
  username: str = payload.get("username")
  email: str = payload.get("email")
  if username is None or email is None or user_id is None:
    raise InvalidCredentialsError(message="Could not validate credentials")

  return payload
