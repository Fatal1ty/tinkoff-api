from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

import ciso8601
from mashumaro import DataClassJSONMixin
from mashumaro.types import SerializableType


FigiName = str
TickerName = str


class BaseModel(DataClassJSONMixin):
    pass


@dataclass
class Error(BaseModel):
    message: Optional[str] = None
    code: Optional[str] = None


class Status(Enum):
    OK = 'Ok'
    ERROR = 'Error'


class Currency(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUS = 'EUR'
    GBP = 'GBP'
    HKD = 'HKD'
    CHF = 'CHF'
    JPY = 'JPY'
    CNY = 'CNY'
    TRY = 'TRY'


class InstrumentType(Enum):
    STOCK = 'Stock'
    CURRENCY = 'Currency'
    BOND = 'Bond'
    ETF = 'Etf'


@dataclass
class MoneyAmount(BaseModel):
    currency: Currency
    value: float


class ISODateTime(datetime, SerializableType):

    def _serialize(self):
        return self.isoformat()

    @classmethod
    def _deserialize(cls, value):
        dt = ciso8601.parse_datetime(value)
        return cls(
            dt.year, dt.month, dt.day, dt.hour, dt.minute,
            dt.second, dt.microsecond, dt.tzinfo
        )
