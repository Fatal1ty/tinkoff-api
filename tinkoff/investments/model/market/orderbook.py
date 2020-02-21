from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

from tinkoff.investments.model.base import BaseModel, FigiName


class TradingStatus(Enum):
    NORMAL_TRADING = 'NormalTrading'
    NOT_AVAILABLE_FOR_TRADING = 'NotAvailableForTrading'


@dataclass
class OrderBookEntity(BaseModel):
    price: float
    quantity: int


@dataclass
class OrderBook(BaseModel):
    figi: FigiName
    depth: int
    bids: List[OrderBookEntity]
    asks: List[OrderBookEntity]
    tradeStatus: TradingStatus
    minPriceIncrement: float
    faceValue: Optional[float] = None
    lastPrice: Optional[float] = None
    closePrice: Optional[float] = None
    limitUp: Optional[float] = None
    limitDown: Optional[float] = None


__all__ = [
    'TradingStatus',
    'OrderBookEntity',
    'OrderBook',
]
