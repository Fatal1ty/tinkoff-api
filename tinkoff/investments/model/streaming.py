from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, ClassVar, Type, TypeVar, Any

from mashumaro import DataClassJSONMixin

from tinkoff.base import classproperty
from tinkoff.investments.model.base import BaseModel, FigiName, ISODateTime
from tinkoff.investments.model.market.candles import Candle, CandleResolution
from tinkoff.investments.model.market.orderbook import OrderBook


class EventName(Enum):
    CANDLE = 'candle'
    ORDERBOOK = 'orderbook'
    INSTRUMENT_INFO = 'instrument_info'
    ERROR = 'error'


class BaseEventKey(DataClassJSONMixin):
    event_name: ClassVar[EventName]

    def subscribe_key(self) -> Dict[str, Any]:
        return {'event': f'{self.event_name.value}:subscribe',
                **self.to_dict()}

    def unsubscribe_key(self) -> Dict[str, Any]:
        return {'event': f'{self.event_name.value}:unsubscribe',
                **self.to_dict()}


@dataclass(unsafe_hash=True)
class CandleEventKey(BaseEventKey):
    event_name = EventName.CANDLE
    figi: FigiName
    interval: CandleResolution


@dataclass(unsafe_hash=True)
class OrderBookEventKey(BaseEventKey):
    event_name = EventName.ORDERBOOK
    figi: FigiName
    depth: int


@dataclass(unsafe_hash=True)
class InstrumentInfoEventKey(BaseEventKey):
    event_name = EventName.INSTRUMENT_INFO
    figi: FigiName


@dataclass(unsafe_hash=True)
class ErrorEventKey(BaseEventKey):
    event_name = EventName.ERROR


ConcreteEventKey = TypeVar('ConcreteEventKey', bound=BaseEventKey)


class BaseEvent(BaseModel):
    event_name: ClassVar[EventName]

    @classproperty
    def key_type(self) -> Type[ConcreteEventKey]:
        return EventKeyMapping[self.event_name]

    def key(self):
        raise NotImplementedError


@dataclass
class CandleEvent(BaseEvent):
    event_name = EventName.CANDLE
    figi: FigiName
    time: ISODateTime
    interval: CandleResolution
    o: float
    c: float
    h: float
    l: float
    v: int

    def key(self):
        return self.key_type(figi=self.figi, interval=self.interval)

    @classmethod
    def from_candle(cls, candle: Candle) -> 'CandleEvent':
        return CandleEvent(
            figi=candle.figi,
            time=candle.time,
            interval=candle.interval,
            o=candle.o,
            c=candle.c,
            h=candle.h,
            l=candle.l,
            v=candle.v
        )


@dataclass
class OrderBookEvent(BaseEvent):
    event_name = EventName.ORDERBOOK
    figi: FigiName
    depth: int
    # TODO: сделать списком сущностей Order
    bids: List[List[float]]
    asks: List[List[float]]

    def key(self):
        return self.key_type(figi=self.figi, depth=self.depth)

    @classmethod
    def from_orderbook(cls, orderbook: OrderBook) -> 'OrderBookEvent':
        return OrderBookEvent(
            figi=orderbook.figi,
            depth=orderbook.depth,
            bids=[[e.price, e.quantity] for e in orderbook.bids],
            asks=[[e.price, e.quantity] for e in orderbook.asks],
        )


@dataclass
class InstrumentInfoEvent(BaseEvent):
    event_name = EventName.INSTRUMENT_INFO
    figi: FigiName
    min_price_increment: float
    lot: float
    trade_status: str
    accrued_interest: Optional[float] = None
    limit_up: Optional[float] = None
    limit_down: Optional[float] = None

    def key(self):
        return self.key_type(figi=self.figi)


@dataclass
class ErrorEvent(BaseEvent):
    event_name = EventName.ERROR
    error: str
    request_id: Optional[str] = None

    def key(self):
        return self.key_type()


@dataclass
class StreamingMessage(DataClassJSONMixin):
    event: EventName
    time: ISODateTime
    payload: Dict[Any, Any]

    @property
    def parsed_payload(self):
        return EventMapping[self.event].from_dict(self.payload)


EventMapping = {
    EventName.CANDLE: CandleEvent,
    EventName.ORDERBOOK: OrderBookEvent,
    EventName.INSTRUMENT_INFO: InstrumentInfoEvent,
    EventName.ERROR: ErrorEvent,
}


EventKeyMapping = {
    EventName.CANDLE: CandleEventKey,
    EventName.ORDERBOOK: OrderBookEventKey,
    EventName.INSTRUMENT_INFO: InstrumentInfoEventKey,
    EventName.ERROR: ErrorEventKey
}
