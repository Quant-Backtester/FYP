# STL

# External
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

# Custom
from utils.security import (
  authenticate_user,
  generate_verify_url,
  hash_password,
)
from utils.jwt_setup import (
  create_access_token,
  create_verification_token,
  verify_verification_token,
)
from .dependencies import get_current_user
from .schemas import CurrentUser, JwtToken, UserPublic, UserCreate, LoginRequest, AccessToken
from background.tasks import send_email_task
from database.sql_db import get_session
from database.models import User
from database.sql_statement import is_existing_user, get_user_by_email
from common.exceptions import (
  InvalidCredentialsError,
  NotFoundError,
  ConflictError,
)


auth_router = APIRouter(prefix="/auth", tags=["Authentication endpoints"])


@auth_router.post(
  path="/send-again",
  status_code=status.HTTP_200_OK,
)
def reverify_email(
  user: UserPublic,
  session: Session = Depends(dependency=get_session),
) -> Response:
  """reverify your email if that particular email is not verified"""
  db_user: User | None = get_user_by_email(session=session, email=user.email)
  if not db_user:
    raise NotFoundError(message="User not found")

  if db_user.is_verified:
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  token: str = create_verification_token(email=db_user.email, username=db_user.username)

  verify_url: str = generate_verify_url(host_prefix=auth_router.prefix, token=token)

  send_email_task.delay(
    subject="Reverify you email", to_email=db_user.email, body=verify_url
  )

  return Response(content="Please check your email", status_code=status.HTTP_200_OK)


@auth_router.post(path="/register", status_code=status.HTTP_201_CREATED)
def register(
  user: UserCreate,
  session: Session = Depends(dependency=get_session),
):
  """register a new user, it will also send a verification token through email"""

  if is_existing_user(session=session, username=user.username, email=user.email):
    raise ConflictError(message="user already exist")

  db_user = User(
    username=user.username,
    email=user.email,
    hashed_password=hash_password(password=user.password),
  )
  session.add(instance=db_user)
  session.flush()

  token: str = create_verification_token(email=db_user.email, username=db_user.username)

  verify_url: str = generate_verify_url(host_prefix=auth_router.prefix, token=token)

  send_email_task.delay(
    subject="Verify your email", to_email=db_user.email, body=verify_url
  )

  return Response(
    status_code=status.HTTP_200_OK,
    content="register sucessfully! Please verify your account",
  )


@auth_router.post(
  path="/login", response_model=AccessToken, status_code=status.HTTP_200_OK
)
def login(
  form_data: LoginRequest, session: Session = Depends(dependency=get_session)
) -> AccessToken:
  """login the user (only verified user can login)"""
  user: User = authenticate_user(
    session=session, email=form_data.email, password=form_data.password
  )
  if not user or not user.is_verified:
    raise InvalidCredentialsError(message="Invalid Credentials")

  if form_data.rememberMe:
    exp = datetime.now() + timedelta(days=30)
  else:
    exp = datetime.now() + timedelta(hours=)
  access_token: str = create_access_token(data=token_data)

  return AccessToken(token_type="bearer", access_token=access_token)


@auth_router.get(path="/me", response_model=CurrentUser, status_code=status.HTTP_200_OK)
def get_yourself(
  payload: CurrentUser = Depends(dependency=get_current_user),
) -> CurrentUser:
  return payload


@auth_router.get(path="/verify-email", status_code=status.HTTP_200_OK)
def verify_email(
  token: str, session: Session = Depends(dependency=get_session)
) -> Response:
  """verify email using the token link"""
  email: str = verify_verification_token(token=token)

  user: User | None = get_user_by_email(session=session, email=email)
  if not user:
    raise NotFoundError(message="User not found")

  if user.is_verified:
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  user.is_verified = True
  session.add(instance=user)
  return Response(status_code=status.HTTP_200_OK, content="Email verified successfully")


__all__ = ("auth_router",)
