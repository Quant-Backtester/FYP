from datetime import datetime
from typing import TypedDict, Required, NotRequired


class JwtToken(TypedDict):
  email: Required[str]
  sub: Required[str]
  exp: NotRequired[datetime]
  
  
class CurrentUser(TypedDict):
  sub: str
  email: str
  


__all__ = (
  "JwtToken",
  "CurrentUser",
)