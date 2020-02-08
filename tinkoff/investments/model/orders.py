from dataclasses import dataclass
from enum import Enum
from typing import Optional

from tinkoff.investments.model.base import BaseModel, FigiName, MoneyAmount
from tinkoff.investments.model.operations import OperationType


OrderID = str


class OrderStatus(Enum):
    NEW = 'New'
    PARTIALLY_FILL = 'PartiallyFill'
    FILL = 'Fill'
    CANCELLED = 'Cancelled'
    REPLACED = 'Replaced'
    PENDING_CANCEL = 'PendingCancel'
    REJECTED = 'Rejected'
    PENDING_REPLACE = 'PendingReplace'
    PENDING_NEW = 'PendingNew'


class OrderType(Enum):
    LIMIT = 'Limit'
    MARKET = 'Market'


@dataclass
class Order(BaseModel):
    orderId: OrderID
    figi: FigiName
    operation: OperationType
    status: OrderStatus
    requestedLots: int
    executedLots: int
    type: OrderType
    price: float


@dataclass
class LimitOrderRequest(BaseModel):
    lots: int
    operation: OperationType
    price: float


@dataclass
class PlacedLimitOrder(BaseModel):
    orderId: OrderID
    operation: OperationType
    status: OrderStatus
    requestedLots: int
    executedLots: int
    rejectReason: Optional[str] = None
    message: Optional[str] = None
    commission: Optional[MoneyAmount] = None


@dataclass
class MarketOrderRequest(BaseModel):
    lots: int
    operation: OperationType


@dataclass
class PlacedMarketOrder(BaseModel):
    orderId: OrderID
    operation: OperationType
    status: OrderStatus
    requestedLots: int
    executedLots: int
    rejectReason: Optional[str] = None
    message: Optional[str] = None
    commission: Optional[MoneyAmount] = None


__all__ = [
    'OrderID',
    'OrderStatus',
    'OrderType',
    'Order',
    'LimitOrderRequest',
    'PlacedLimitOrder',
    'MarketOrderRequest',
    'PlacedMarketOrder',
]
