from dataclasses import dataclass
from enum import Enum

from tinkoff.investments.model.base import BaseModel


BrokerAccountID = str


class BrokerAccountType(Enum):
    TINKOFF = 'Tinkoff'
    TINKOFF_IIS = 'TinkoffIis'


__all__ = [
    'BrokerAccountID',
    'BrokerAccountType',
]
