from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarketDataPayload:
    price: float
    volume: int

@dataclass(frozen=True, slots=True)
class OrderFillPayload:
    order_id: str
    fill_price: float
    quantity: int