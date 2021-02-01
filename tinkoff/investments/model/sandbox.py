from dataclasses import dataclass

from tinkoff.investments.model.base import BaseModel, Currency, FigiName
from tinkoff.investments.model.user.accounts import (
    BrokerAccountID,
    BrokerAccountType,
)


@dataclass
class SandboxAccount(BaseModel):
    brokerAccountType: BrokerAccountType
    brokerAccountId: BrokerAccountID


@dataclass
class SandboxAccountRegisterRequest(BaseModel):
    brokerAccountType: BrokerAccountType


@dataclass
class SandboxSetCurrencyBalanceRequest(BaseModel):
    currency: Currency
    balance: float


@dataclass
class SandboxSetPositionBalanceRequest(BaseModel):
    figi: FigiName
    balance: float


__all__ = [
    "SandboxAccount",
    "SandboxAccountRegisterRequest",
    "SandboxSetCurrencyBalanceRequest",
    "SandboxSetPositionBalanceRequest",
]
