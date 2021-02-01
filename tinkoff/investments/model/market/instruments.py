from dataclasses import dataclass
from typing import List, Optional

from tinkoff.investments.model.base import (
    BaseModel,
    Currency,
    FigiName,
    InstrumentType,
    TickerName,
)


@dataclass
class MarketInstrument(BaseModel):
    figi: FigiName
    ticker: TickerName
    lot: int
    name: str
    type: InstrumentType
    currency: Optional[Currency] = None
    isin: Optional[str] = None
    minPriceIncrement: Optional[float] = None
    minQuantity: Optional[int] = None


@dataclass
class MarketInstrumentList(BaseModel):
    total: int
    instruments: List[MarketInstrument]


__all__ = [
    "MarketInstrument",
    "MarketInstrumentList",
]
