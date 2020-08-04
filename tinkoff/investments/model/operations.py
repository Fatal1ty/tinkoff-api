from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from tinkoff.investments.model.base import (
    BaseModel,
    ISODateTime,
    MoneyAmount,
    Currency,
    FigiName,
    InstrumentType,
)


OperationID = str
TradeID = str


class OperationStatus(Enum):
    DONE = 'Done'
    DECLINE = 'Decline'
    PROGRESS = 'Progress'


class OperationType(Enum):
    BUY = 'Buy'
    SELL = 'Sell'


class OperationTypeWithCommission(Enum):
    BUY = 'Buy'
    BUY_CARD = 'BuyCard'
    SELL = 'Sell'
    BROKER_COMMISSION = 'BrokerCommission'
    EXCHANGE_COMMISSION = 'ExchangeCommission'
    SERVICE_COMMISSION = 'ServiceCommission'
    MARGIN_COMMISSION = 'MarginCommission'
    OTHER_COMMISSION = 'OtherCommission'
    PAY_IN = 'PayIn'
    PAY_OUT = 'PayOut'
    TAX = 'Tax'
    TAX_LUCRE = 'TaxLucre'
    TAX_DIVIDEND = 'TaxDividend'
    TAX_COUPON = 'TaxCoupon'
    TAX_BACK = 'TaxBack'
    REPAYMENT = 'Repayment'
    PART_REPAYMENT = 'PartRepayment'
    COUPON = 'Coupon'
    DIVIDEND = 'Dividend'
    SECURITY_IN = 'SecurityIn'
    SECURITY_OUT = 'SecurityOut'


@dataclass
class OperationTrade(BaseModel):
    tradeId: TradeID
    date: ISODateTime
    price: float
    quantity: int


@dataclass
class Operation(BaseModel):
    id: OperationID
    status: OperationStatus
    currency: Currency
    payment: float
    isMarginCall: bool
    date: ISODateTime
    trades: Optional[List[OperationTrade]] = None
    commission: Optional[MoneyAmount] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    figi: Optional[FigiName] = None
    instrumentType: Optional[InstrumentType] = None
    operationType: Optional[OperationTypeWithCommission] = None
    quantityExecuted: Optional[int] = None


@dataclass
class Operations(BaseModel):
    operations: List[Operation]


__all__ = [
    'OperationID',
    'TradeID',
    'OperationStatus',
    'OperationType',
    'OperationTypeWithCommission',
    'OperationTrade',
    'Operation',
    'Operations',
]
