from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from tinkoff.investments.model.base import BaseModel, FigiName


class CandleResolution(Enum):
    MIN_1 = "1min"
    MIN_2 = "2min"
    MIN_3 = "3min"
    MIN_5 = "5min"
    MIN_10 = "10min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


@dataclass
class Candle(BaseModel):
    figi: FigiName
    interval: CandleResolution
    # TODO: сделать алиасы на понятные названия
    o: float
    c: float
    h: float
    l: float
    v: int
    time: datetime = field(metadata={"deserialize": "ciso8601"})


@dataclass
class Candles(BaseModel):
    figi: FigiName
    interval: CandleResolution
    candles: List[Candle]


__all__ = [
    "CandleResolution",
    "Candle",
    "Candles",
]
