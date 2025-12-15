#external
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

#Custom
from configs import settings
from custom.custom_type import CurrentUser


async def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(dependency=HTTPBearer()),
) -> CurrentUser:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  payload: CurrentUser = jwt.decode(
    jwt=credentials.credentials,
    key=settings.jwt_secret_key,
    algorithms=[settings.algorithm],
  )
  username: str = payload.get("sub")
  email: str = payload.get("email")
  if username is None or email is None:
    raise credentials_exception

  return payload
