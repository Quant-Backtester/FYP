from datetime import datetime
from typing import Any, TypedDict, ReadOnly, NotRequired, Required


class LoggingType(TypedDict):
  timestamp: str
  level: str
  logger: str
  module: str
  function: str
  line: int
  message: str
  exception: NotRequired[str]
  
class LogError(TypedDict):
  status_code: Required[int]
  duration_ms: float
  
  
class LogResponse(TypedDict):
  status_code: Required[int]
  duration_ms: float
  
class LogRequest(TypedDict):
  method: Required[int]
  url: Required[int]
  query_params: NotRequired[dict[str, Any]]
  path_params: NotRequired[dict[str, Any]]
  headers: NotRequired[dict[str, Any]]
  client_ip: str
  user_agent: str
  body: NotRequired[dict[str, Any]]
  