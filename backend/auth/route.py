from email.utils import 


from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from .security import authenticate_user, hash_password  
from .jwt_setup import create_access_token, get_current_user, create_verification_token, verify_verification_token
from .auth_model import UserPublic, UserCreate, LoginRequest
from core import settings
from models import User
from core import send_email

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserPublic)
def register(user: UserCreate, session: Session = Depends(get_session)):
    #TODO validate email

    existing_user = session.exec(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    token = create_verification_token(db_user.email)
    verify_url = f"http://{settings.host}:{settings.port}{auth_router.prefix}/verify-email?token={token}"
    send_email(
        to_email=db_user.email,
        subject="Verify your email",
        body=f"Click to verify: {verify_url}"
    )
    return db_user

@auth_router.post("/login")
def login(form_data: LoginRequest, session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your inbox."
        )
    access_token = create_access_token(data={"sub": user.username, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserPublic)
def read_users_me(payload: dict = Depends(get_current_user)):
    return {
        "username": payload["sub"],
        "email": payload.get("email")
    }


@auth_router.get("/verify-email")
def verify_email(token: str, session: Session = Depends(get_session)):
    email = verify_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    session.add(user)
    session.commit()
    return {"message": "Email verified successfully"}