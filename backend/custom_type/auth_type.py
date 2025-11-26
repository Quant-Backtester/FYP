from datetime import datetime
from typing import TypedDict, NamedTuple, Required, NotRequired


class JwtToken(TypedDict):
  email: Required[str]
  sub: Required[str]
  exp: NotRequired[datetime]
  
  
class CurrentUser(TypedDict):
    sub: str
    email: str