from dataclasses import dataclass

# custom
from .event_enum import EventEnum


@dataclass(frozen=True, slots=True)
class Event[T]:
    timestamp: int
    event_type: EventEnum
    paylaod: T
