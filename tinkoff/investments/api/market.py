from datetime import datetime, timezone
from typing import Optional, List, Any

from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI

from tinkoff.investments.client.exceptions import TinkoffInvestmentsUsageError
from tinkoff.investments.model.base import FigiName, TickerName
from tinkoff.investments.model.market.orderbook import OrderBook
from tinkoff.investments.model.market.candles import (
    Candle,
    Candles,
    CandleResolution,
)
from tinkoff.investments.model.market.instruments import (
    MarketInstrument,
    MarketInstrumentList,
)


class MarketInstrumentsAPI(BaseTinkoffInvestmentsAPI):
    async def search(
            self,
            figi: Optional[FigiName] = None,
            ticker: Optional[TickerName] = None
    ) -> List[MarketInstrument]:

        if figi:
            search_method = 'by-figi'
            params = {'figi': figi}
        elif ticker:
            search_method = 'by-ticker'
            params = {'ticker': ticker}
        else:
            raise TinkoffInvestmentsUsageError('Expected either figi or ticker')
        return await self.__get_instruments(
            path=f'/market/search/{search_method}',
            **params
        )

    async def get_stocks(self) -> List[MarketInstrument]:
        return await self.__get_instruments('/market/stocks')

    async def get_bonds(self) -> List[MarketInstrument]:
        return await self.__get_instruments('/market/bonds')

    async def get_etfs(self) -> List[MarketInstrument]:
        return await self.__get_instruments('/market/etfs')

    async def get_currencies(self) -> List[MarketInstrument]:
        return await self.__get_instruments('/market/currencies')

    async def __get_instruments(self, path, **params):
        # type: (str, Any) -> List[MarketInstrument]
        payload = await self._request(
            method='GET',
            path=path,
            params=params,
        )
        return MarketInstrumentList.from_dict(payload).instruments


class MarketOrderBooksAPI(BaseTinkoffInvestmentsAPI):
    async def get(self, figi: FigiName, depth: int) -> OrderBook:
        payload = await self._request(
            method='GET',
            path='/market/orderbook',
            params={
                'figi': figi,
                'depth': depth,
            }
        )
        return OrderBook.from_dict(payload)


class MarketCandlesAPI(BaseTinkoffInvestmentsAPI):
    async def get(self, figi, dt_from, dt_to, interval):
        # type: (FigiName, datetime, datetime, CandleResolution) -> List[Candle]
        if not dt_from.tzinfo:
            dt_from = dt_from.replace(tzinfo=timezone.utc)
        if not dt_to.tzinfo:
            dt_to = dt_to.replace(tzinfo=timezone.utc)
        payload = await self._request(
            method='GET',
            path='/market/candles',
            params={
                'figi': figi,
                'from': dt_from.isoformat(),
                'to': dt_to.isoformat(),
                'interval': interval.value,
            },
        )
        return Candles.from_dict(payload).candles


class MarketAPI(BaseTinkoffInvestmentsAPI):
    def __init__(self, *args, **kwargs):
        super(MarketAPI, self).__init__(*args, **kwargs)
        self.instruments = MarketInstrumentsAPI(*args, **kwargs)
        self.orderbooks = MarketOrderBooksAPI(*args, **kwargs)
        self.candles = MarketCandlesAPI(*args, **kwargs)
