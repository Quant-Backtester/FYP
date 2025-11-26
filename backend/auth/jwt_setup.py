# STL
from datetime import datetime, timedelta, timezone

#third party
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

#custom
from custom_type import JwtToken
from core import settings

def create_access_token(data: JwtToken) -> str:
    to_encode: JwtToken = {
        "sub": data["sub"],
        "email": data["email"],
        "exp": datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
    }
    return jwt.encode(payload=to_encode, key=settings.jwt_secret_key, algorithm=settings.algorithm) # type: ignore


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(dependency=HTTPBearer())
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = jwt.decode(
        jwt=credentials.credentials,
        key=settings.jwt_secret_key,
        algorithms=[settings.algorithm]
    )
    print(payload)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return payload


def create_verification_token(email: str) -> str:
    """Create a short-lived token for email verification."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    return jwt.encode(
        {"sub": email, "exp": expire, "type": "verification"},
        settings.jwt_secret_key,
        algorithm=settings.algorithm
    )

def verify_verification_token(token: str) -> str | None:
    """Return email if valid, None otherwise."""
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.algorithm])
    if payload.get("type") != "verification":
        return None
    return payload.get("sub")