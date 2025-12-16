from datetime import datetime
from typing import NotRequired, TypedDict, Required


#Custom
from custom.custom_enums import PayloadEnum


class JwtToken(TypedDict):
  """ Token for login """
  sub: Required[str]
  username: Required[str]
  email: Required[str]
  exp: NotRequired[datetime]


class CurrentUser(TypedDict):
  """ for identifying the current user """
  username: Required[str]
  email: Required[str]


class VerificationToken(TypedDict):
  """ Token for verification (or other) """
  username: Required[str]
  email: Required[str]
  exp: Required[datetime]
  what: Required[PayloadEnum]


class VerifyResponseMessage(TypedDict):
  message: str
  status_code: int

__all__ = (
  "JwtToken",
  "CurrentUser",
  "VerificationToken",
  "VerifyResponseMessage",
)
