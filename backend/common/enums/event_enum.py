from enum import StrEnum, auto


class EventEnum(StrEnum):
  REQUEST = auto()
  RESPONSE = auto()
  ERROR = auto()

