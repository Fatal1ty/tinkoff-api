import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Type, Optional, Callable, List

from aiohttp import ClientWebSocketResponse, WSMsgType, ClientError

from tinkoff.base import BaseHTTPClient
from tinkoff.investments.client.environments import Environment, EnvironmentURL
from tinkoff.investments.model.streaming import (
    BaseEvent,
    CandleEvent,
    OrderBookEvent,
    InstrumentInfoEvent,
    ErrorEvent,
    BaseEventKey,
    StreamingMessage,
    EventName,
)


logger = logging.getLogger('streaming-api')


class BaseEventStream:
    EVENT_TYPE: Type[BaseEvent] = None

    def __init__(self):
        self._subscribers = {}  # type: Dict[BaseEventKey, Callable]
        self._client = None  # type: Optional[TinkoffInvestmentsStreamingClient]

    def __call__(self, *args, **kwargs):
        def decorator(callback):
            self._subscribers[
                self.EVENT_TYPE.key_type(*args, **kwargs)] = callback
            return callback
        return decorator

    async def subscribe(self, callback, *args, **kwargs):
        key = self.EVENT_TYPE.key_type(*args, **kwargs)
        self._subscribers[key] = callback
        await self._client.request(key.subscribe_key())

    async def unsubscribe(self, *args, **kwargs):
        key = self.EVENT_TYPE.key_type(*args, **kwargs)
        self._subscribers.pop(key, None)
        await self._client.request(key.unsubscribe_key())

    async def publish(self, event: BaseEvent, server_time: datetime):
        callback = self._subscribers.get(event.key())  # TODO: сделать иначе
        if callback:
            await callback(event, server_time)


class CandleEventStream(BaseEventStream):
    EVENT_TYPE = CandleEvent


class OrderBookEventStream(BaseEventStream):
    EVENT_TYPE = OrderBookEvent


class InstrumentInfoEventStream(BaseEventStream):
    EVENT_TYPE = InstrumentInfoEvent


class ErrorEventStream(BaseEventStream):
    EVENT_TYPE = ErrorEvent


class EventsBroker:
    def __init__(self):
        self.candles = CandleEventStream()
        self.orderbooks = OrderBookEventStream()
        self.instrument_info = InstrumentInfoEventStream()
        self.errors = ErrorEventStream()

        self._routes = {
            EventName.CANDLE: self.candles,
            EventName.ORDERBOOK: self.orderbooks,
            EventName.INSTRUMENT_INFO: self.instrument_info,
            EventName.ERROR: self.errors,
        }

    def add_publisher(self, client: 'TinkoffInvestmentsStreamingClient'):
        self.candles._client = client
        self.orderbooks._client = client
        self.instrument_info._client = client
        self.errors._client = client

    async def publish(self, event: BaseEvent, server_time: datetime):
        await self._routes[event.event_name].publish(event, server_time)


class TinkoffInvestmentsStreamingClient(BaseHTTPClient):
    def __init__(
            self,
            token: str,
            events: EventsBroker = None,
            receive_timeout: Optional[float] = 5,
            heartbeat: Optional[float] = 3,
            reconnect_timeout: float = 3,
    ):
        super().__init__(
            base_url=EnvironmentURL[Environment.STREAMING],
            headers={
                'authorization': f'Bearer {token}'
            }
        )
        self.events = events or EventsBroker()
        self.events.add_publisher(self)
        self._ws = None  # type: Optional[ClientWebSocketResponse]
        self._receive_timeout = receive_timeout
        self._heartbeat = heartbeat
        self._reconnect_timeout = reconnect_timeout

    async def request(self, key: Dict[str, Any]):
        if self._ws:
            await self._ws.send_json(key)

    async def run(self):
        while not self.closed:
            if self._session.closed:
                return
            try:
                async with self._session.ws_connect(
                    url=self._base_url,
                    timeout=0.,
                    receive_timeout=self._receive_timeout,
                    heartbeat=self._heartbeat,
                ) as ws:
                    self._ws = ws
                    await self._run(ws)
            except asyncio.TimeoutError:
                await asyncio.sleep(self._reconnect_timeout)
            except ClientError:
                await asyncio.sleep(self._reconnect_timeout)

    async def _run(self, ws: ClientWebSocketResponse):
        await self._subscribe_to_streams(ws)
        async for msg in ws:
            # noinspection PyUnresolvedReferences
            if msg.type == WSMsgType.TEXT:
                # noinspection PyUnresolvedReferences
                msg = StreamingMessage.from_json(msg.data)
                try:
                    await self.events.publish(
                        event=msg.parsed_payload,
                        server_time=msg.time,
                    )
                except Exception as e:
                    logger.exception(
                        'Unhandled exception in streaming event handler: %s', e
                    )

    async def _subscribe_to_streams(self, ws: ClientWebSocketResponse):
        coros = (ws.send_json(key) for key in self._subscription_keys())
        await asyncio.gather(*coros)

    @property
    def _event_streams(self):
        return (self.events.candles, self.events.orderbooks,
                self.events.instrument_info)

    def _subscription_keys(self) -> List[Dict[str, Any]]:
        keys = []
        for event_stream in self._event_streams:
            # noinspection PyProtectedMember
            keys.extend([key.subscribe_key()
                         for key in event_stream._subscribers.keys()])
        return keys


__all__ = [
    'EventsBroker',
    'TinkoffInvestmentsStreamingClient'
]
