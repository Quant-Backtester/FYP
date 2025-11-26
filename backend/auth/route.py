#STL

#External
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

#Custom
from custom_type import JwtToken
from database import get_session
from .security import authenticate_user, generate_verify_url, hash_password, is_existing_user
from .jwt_setup import create_access_token, get_current_user, create_verification_token, verify_verification_token
from .auth_model import UserPublic, UserCreate, LoginRequest
from custom_type import CurrentUser
from models import User
from core import send_email

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post(path="/register", response_model=UserPublic)
def register(user: UserCreate, session: Session = Depends(dependency=get_session)) -> User:
    """register a new user, it will also send a verification token through email"""
    
    if is_existing_user(session=session, username=user.username, email=user.email):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(password=user.password)
    )
    session.add(instance=db_user)
    session.commit()
    session.refresh(instance=db_user)

    token: str = create_verification_token(email=db_user.email)
    
    verify_url = generate_verify_url(host_prefix=auth_router.prefix, token=token)
    
    send_email(
        to_email=db_user.email,
        subject="Verify your email",
        body=f"Click to verify: {verify_url}"
    )
    return db_user

@auth_router.post(path="/login")
def login(form_data: LoginRequest, session: Session = Depends(dependency=get_session)) -> dict[str, str]:
    """ login the user (only verified user can login)"""
    user = authenticate_user(session, form_data.email, form_data.password)
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
        
    token_data = JwtToken(sub=user.username, email=user.email)
        
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get(path="/me", response_model=UserPublic)
def read_users_me(payload: CurrentUser = Depends(dependency=get_current_user)) -> CurrentUser:
    return payload

@auth_router.get(path="/verify-email")
def verify_email(token: str, session: Session = Depends(dependency=get_session)) -> dict[str, str]:
    """ verify email using the token link """
    email = verify_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    session.add(instance=user)
    return {"message": "Email verified successfully"}