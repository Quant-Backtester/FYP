# External
from pydantic import BaseModel


class LoginRequest(BaseModel):
  email: str
  password: str


class UserCreate(BaseModel):
  username: str
  email: str
  password: str


class UserPublic(BaseModel):
  username: str
  email: str


class AccessToken(BaseModel):
  access_token: str
  token_type: str




__all__ = ("LoginRequest", "UserCreate", "UserPublic", "AccessToken")
