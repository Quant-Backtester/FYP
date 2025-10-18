# STL
from typing import Dict
from datetime import datetime, timedelta, timezone

#third party
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

#custom
from core import settings

def create_access_token(data) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.algorithm)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except jwt.PyJWTError:
        raise credentials_exception
    
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
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "verification":
            return None
        return payload.get("sub")
    except jwt.PyJWTError:
        return None