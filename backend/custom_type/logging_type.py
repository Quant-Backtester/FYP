from typing import Literal, TypedDict, NotRequired, Required


class LoggingType(TypedDict):
  timestamp: str
  level: str
  logger: str
  module: str
  function: str
  line: int
  message: str
  exception: NotRequired[str]
  
  
  
class HttpRequestLog[T](TypedDict):
    msg: Literal["HTTP Request"]
    event: str
    method: Required[str]
    url: Required[str]
    query_params: dict[str, str | list[str]]
    path_params: dict[str, str]
    headers: dict[str, str]
    client_ip: str
    user_agent: str | None
    body: dict[str, T] | str

class HttpResponseLog(TypedDict):
    msg: Literal["HTTP Response"]
    event: str
    status_code: int
    duration_ms: float
    request_id: str

class HttpErrorLog(TypedDict):
    msg: Literal["Request failed"]
    event: str
    status_code: int
    duration_ms: float
    error: str 
    traceback: str
    request_id: NotRequired[str]
  
  
__all__ = (
  "LoggingType",
  "HttpErrorLog",
  "HttpRequestLog",
  "HttpResponseLog"
)
  