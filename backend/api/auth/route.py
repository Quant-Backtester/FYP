# STL

# External
from typing import TypedDict
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select

# Custom
from custom.custom_type import JwtToken, CurrentUser
from .security import (
  authenticate_user,
  generate_verify_url,
  hash_password,
)
from .jwt_setup import (
  create_access_token,
  create_verification_token,
  verify_verification_token,
)
from .dependencies import get_current_user
from .auth_model import UserPublic, UserCreate, LoginRequest, AccessToken
from core import send_email
from database.sql_db import get_session
from database.models import User
from database.sql_statement import is_existing_user, get_user_by_email


class VerifyResponseMessage(TypedDict):
  message: str
  status_code: int


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
  path="/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register(
  user: UserCreate,
  background_tasks: BackgroundTasks,
  session: Session = Depends(dependency=get_session),
) -> User:
  """register a new user, it will also send a verification token through email"""

  if is_existing_user(session=session, username=user.username, email=user.email):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Username or email already registered",
    )

  db_user = User(
    username=user.username,
    email=user.email,
    hashed_password=hash_password(password=user.password),
  )
  session.add(instance=db_user)
  session.flush()

  token: str = create_verification_token(email=db_user.email)

  verify_url: str = generate_verify_url(host_prefix=auth_router.prefix, token=token)

  background_tasks.add_task(
    func=send_email,
    to_email=db_user.email,
    subject="Please Verify your email.",
    body=f"Click to verify: {verify_url}",
  )
  return db_user


@auth_router.post(
  path="/login", response_model=AccessToken, status_code=status.HTTP_200_OK
)
def login(
  form_data: LoginRequest, session: Session = Depends(dependency=get_session)
) -> AccessToken:
  """login the user (only verified user can login)"""
  user: User | None = authenticate_user(
    session=session, username=form_data.email, password=form_data.password
  )
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  if not user.is_verified:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Email not verified. Please check your inbox.",
    )

  token_data = JwtToken(sub=user.username, email=user.email)

  access_token = create_access_token(data=token_data)

  return AccessToken(access_token=access_token, token_type="bearer")


@auth_router.get(path="/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
def read_users_me(
  payload: CurrentUser = Depends(dependency=get_current_user),
) -> CurrentUser:
  return payload


@auth_router.get(path="/verify-email", status_code=status.HTTP_200_OK)
def verify_email(
  token: str, session: Session = Depends(dependency=get_session)
) -> VerifyResponseMessage:
  """verify email using the token link"""
  email: str | None = verify_verification_token(token)
  if not email:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
    )

  user: User | None = get_user_by_email(session=session, email=email)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  if user.is_verified:
    return VerifyResponseMessage(
      status_code=status.HTTP_401_UNAUTHORIZED, message="Email already verified"
    )

  user.is_verified = True
  session.add(instance=user)
  return VerifyResponseMessage(
    status_code=status.HTTP_200_OK, message="Email verified successfully"
  )


__all__ = ("auth_router",)
