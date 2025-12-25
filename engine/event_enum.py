from enum import StrEnum, auto


class EventEnum(StrEnum):
    MARKET_DATA = auto()
    ORDER_SUBMIT = auto()
    ORDER_FILL = auto()
    ORDER_CANCEL = auto()
    TIMER = auto()
