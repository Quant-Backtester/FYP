# External
from typing import Literal
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
  email: str
  password: str
  rememberMe: bool


class UserCreate(BaseModel):
  username: str
  email: str
  password: str


class UserPublic(BaseModel):
  username: str
  email: str


class AccessToken(BaseModel):
  access_token: str
  token_type: Literal["bearer"]

class CurrentUser(BaseModel):
  username: str
  email: EmailStr

class JwtToken(BaseModel):
  sub: str
  username: str
  email: EmailStr
  exp: int | None = None
  iat: int



