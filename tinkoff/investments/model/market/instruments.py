from dataclasses import dataclass
from typing import Optional, List

from tinkoff.investments.model.base import BaseModel, Currency


# TODO: вынести в base?
FigiName = str
TickerName = str


@dataclass
class MarketInstrument(BaseModel):
    figi: FigiName
    ticker: TickerName
    lot: int
    name: str
    currency: Optional[Currency] = None
    isin: Optional[str] = None
    minPriceIncrement: float = None


@dataclass
class MarketInstrumentList(BaseModel):
    total: int
    instruments: List[MarketInstrument]


__all__ = [
    'FigiName',
    'TickerName',
    'MarketInstrument',
    'MarketInstrumentList',
]
