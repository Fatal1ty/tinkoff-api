from dataclasses import dataclass
from enum import Enum
from typing import List

from tinkoff.investments.model.base import BaseModel

BrokerAccountID = str


class BrokerAccountType(Enum):
    TINKOFF = "Tinkoff"
    TINKOFF_IIS = "TinkoffIis"


@dataclass
class UserAccount(BaseModel):
    brokerAccountType: BrokerAccountType
    brokerAccountId: BrokerAccountID


@dataclass
class UserAccounts(BaseModel):
    accounts: List[UserAccount]


__all__ = [
    "BrokerAccountID",
    "BrokerAccountType",
    "UserAccount",
    "UserAccounts",
]
