from datetime import datetime, timedelta
from typing import AsyncIterator

from tinkoff.investments import (
    Candle, CandleResolution, FigiName, TinkoffInvestmentsRESTClient
)


class HistoricalData:
    _TIMEDELTA = {
        'MIN': timedelta(days=1),
        'HOUR': timedelta(weeks=1),
        'DAY': timedelta(days=365),
        'WEEK': timedelta(days=728),
        'MONTH': timedelta(days=365 * 10),
    }

    def __init__(self, client: TinkoffInvestmentsRESTClient):
        self._client = client

    async def iter_candles(
        self,
        figi: FigiName,
        dt_from: datetime,
        dt_to: datetime,
        interval: CandleResolution
    ) -> AsyncIterator[Candle]:
        days = (dt_to - dt_from).days
        delta = self._get_timedelta(interval)
        for days_increment in range(0, days, delta.days):
            if dt_from + timedelta(days=days_increment) > datetime.utcnow():
                break
            for candle in await self._client.market.candles.get(
                figi=figi,
                dt_from=dt_from + timedelta(days=days_increment),
                dt_to=dt_from + timedelta(days=days_increment + delta.days),
                interval=interval
            ):
                yield candle
        await self._client.close()

    def _get_timedelta(self, interval: CandleResolution) -> timedelta:
        for key, value in self._TIMEDELTA.items():
            if interval.name.startswith(key):
                return value
        raise ValueError(f'Unknown interval {interval}')
