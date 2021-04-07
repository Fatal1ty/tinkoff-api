from dataclasses import dataclass
from enum import Enum
from typing import Optional

from mashumaro import DataClassJSONMixin

FigiName = str
TickerName = str


class BaseModel(DataClassJSONMixin):
    pass


@dataclass
class Error(BaseModel):
    message: Optional[str] = None
    code: Optional[str] = None


class Status(Enum):
    OK = "Ok"
    ERROR = "Error"


class Currency(Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    HKD = "HKD"
    CHF = "CHF"
    JPY = "JPY"
    CNY = "CNY"
    TRY = "TRY"


class InstrumentType(Enum):
    STOCK = "Stock"
    CURRENCY = "Currency"
    BOND = "Bond"
    ETF = "Etf"


@dataclass
class MoneyAmount(BaseModel):
    currency: Currency
    value: float
