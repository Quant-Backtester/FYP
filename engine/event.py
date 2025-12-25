from dataclasses import dataclass

# custom
from .event_enum import EventEnum


@dataclass(frozen=True)
class Event[T]:
    timestamp: int
    event_type: EventEnum
    paylao: dict[str, T]
