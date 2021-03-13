from typing import List

from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.portfolio import (
    Currencies,
    CurrencyPosition,
    Portfolio,
    PortfolioPosition,
)
from tinkoff.investments.model.user.accounts import BrokerAccountID


class PortfolioAPI(BaseTinkoffInvestmentsAPI):
    async def get_positions(self, broker_account_id=None):
        # type: (BrokerAccountID) -> List[PortfolioPosition]
        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}
        payload = await self._request(
            method="GET",
            path="/portfolio",
            params=params,
        )
        return Portfolio.from_dict(payload).positions  # type: ignore

    async def get_currencies(self, broker_account_id=None):
        # type: (BrokerAccountID) -> List[CurrencyPosition]
        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}
        payload = await self._request(
            method="GET",
            path="/portfolio/currencies",
            params=params,
        )
        return Currencies.from_dict(payload).currencies  # type: ignore
