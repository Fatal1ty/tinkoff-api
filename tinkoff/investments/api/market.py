from datetime import datetime
from typing import Any, List, Optional

from tinkoff.base import RateLimiter
from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.client.exceptions import TinkoffInvestmentsAPIError
from tinkoff.investments.model.base import FigiName, TickerName
from tinkoff.investments.model.market.candles import (
    Candle,
    CandleResolution,
    Candles,
)
from tinkoff.investments.model.market.instruments import (
    MarketInstrument,
    MarketInstrumentList,
)
from tinkoff.investments.model.market.orderbook import OrderBook
from tinkoff.investments.utils import offset_aware_datetime


class MarketInstrumentsAPI(BaseTinkoffInvestmentsAPI):
    def _get_default_rate_limiter(self) -> RateLimiter:
        return RateLimiter(rate=240, period=60)

    async def search(self, ticker: TickerName) -> List[MarketInstrument]:
        return await self.__get_instruments(
            path="/market/search/by-ticker",
            ticker=ticker,
        )

    async def get(self, figi: FigiName) -> Optional[MarketInstrument]:
        try:
            payload = await self._request(
                method="GET",
                path="/market/search/by-figi",
                params={"figi": figi},
            )
            return MarketInstrument.from_dict(payload)  # type: ignore
        except TinkoffInvestmentsAPIError as e:
            if e.error.code == "NOT_FOUND":
                return None
            else:
                raise e from None

    async def get_stocks(self) -> List[MarketInstrument]:
        return await self.__get_instruments("/market/stocks")

    async def get_bonds(self) -> List[MarketInstrument]:
        return await self.__get_instruments("/market/bonds")

    async def get_etfs(self) -> List[MarketInstrument]:
        return await self.__get_instruments("/market/etfs")

    async def get_currencies(self) -> List[MarketInstrument]:
        return await self.__get_instruments("/market/currencies")

    async def __get_instruments(self, path, **params):
        # type: (str, Any) -> List[MarketInstrument]
        payload = await self._request(
            method="GET",
            path=path,
            params=params,
        )
        return MarketInstrumentList.from_dict(
            payload  # type: ignore
        ).instruments


class MarketOrderBooksAPI(BaseTinkoffInvestmentsAPI):
    async def get(self, figi: FigiName, depth: int) -> OrderBook:
        payload = await self._request(
            method="GET",
            path="/market/orderbook",
            params={
                "figi": figi,
                "depth": depth,
            },
        )
        return OrderBook.from_dict(payload)  # type: ignore


class MarketCandlesAPI(BaseTinkoffInvestmentsAPI):
    async def get(self, figi, dt_from, dt_to, interval):
        # type: (FigiName, datetime, datetime, CandleResolution) -> List[Candle]
        dt_from = offset_aware_datetime(dt_from)
        dt_to = offset_aware_datetime(dt_to)
        payload = await self._request(
            method="GET",
            path="/market/candles",
            params={
                "figi": figi,
                "from": dt_from.isoformat(),
                "to": dt_to.isoformat(),
                "interval": interval.value,
            },
        )
        return Candles.from_dict(payload).candles  # type: ignore


class MarketAPI(BaseTinkoffInvestmentsAPI):
    def __init__(self, *args, **kwargs):
        super(MarketAPI, self).__init__(*args, **kwargs)
        self.instruments = MarketInstrumentsAPI(*args, **kwargs)
        self.orderbooks = MarketOrderBooksAPI(*args, **kwargs)
        self.candles = MarketCandlesAPI(*args, **kwargs)
