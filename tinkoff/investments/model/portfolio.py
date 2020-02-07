from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

from tinkoff.investments.model.base import BaseModel, Currency
from tinkoff.investments.model.market.instruments import FigiName, TickerName


class InstrumentType(Enum):
    STOCK = 'Stock'
    CURRENCY = 'Currency'
    BOND = 'Bond'
    ETF = 'Etf'


@dataclass
class MoneyAmount(BaseModel):
    currency: Currency
    value: float


@dataclass
class PortfolioPosition(BaseModel):
    figi: FigiName
    instrumentType: InstrumentType
    balance: float
    lots: int
    name: str
    ticker: Optional[TickerName] = None
    isin: Optional[str] = None
    blocked: Optional[float] = None
    expectedYield: Optional[MoneyAmount] = None
    averagePositionPrice: Optional[MoneyAmount] = None
    averagePositionPriceNoNkd: Optional[MoneyAmount] = None


@dataclass
class CurrencyPosition(BaseModel):
    currency: Currency
    balance: float
    blocked: Optional[float] = None


@dataclass
class Portfolio(BaseModel):
    positions: List[PortfolioPosition]


@dataclass
class Currencies(BaseModel):
    currencies: List[CurrencyPosition]


__all__ = [
    'InstrumentType',
    'MoneyAmount',
    'PortfolioPosition',
    'CurrencyPosition',
    'Portfolio',
    'Currencies',
]
