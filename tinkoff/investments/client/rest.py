import asyncio
from typing import Any, Dict, Optional

from aiohttp import ClientResponseError

from tinkoff.base import BaseHTTPClient, RateLimiter, RateLimitReached
from tinkoff.investments.api import (
    SandboxAPI,
    OrdersAPI,
    PortfolioAPI,
    MarketAPI,
    OperationsAPI,
    UserAPI,
)
from tinkoff.investments.client.environments import Environment, EnvironmentURL
from tinkoff.investments.client.exceptions import (
    TinkoffInvestmentsUnauthorizedError,
    TinkoffInvestmentsTooManyRequestsError,
    TinkoffInvestmentsTimeoutError,
    TinkoffInvestmentsUnavailableError,
)


class TinkoffInvestmentsRESTClient(BaseHTTPClient):
    def __init__(
            self,
            token: str,
            environment: Environment = Environment.PRODUCTION,
            timeout: Optional[float] = 5,
            wait_on_rate_limit: bool = True,
    ):

        super(TinkoffInvestmentsRESTClient, self).__init__(
            base_url=EnvironmentURL[environment],
            headers={
                'authorization': f'Bearer {token}'
            },
            timeout=timeout,
        )
        self.sandbox = SandboxAPI(self)
        self.orders = OrdersAPI(self)
        self.portfolio = PortfolioAPI(self)
        self.market = MarketAPI(self)
        self.operations = OperationsAPI(self)
        self.user = UserAPI(self)
        self.wait_on_rate_limit = wait_on_rate_limit

    async def _request(self, method, path, rate_limit=None, **kwargs):
        # type: (str, str, Optional[RateLimiter], Any) -> Dict[Any, Any]
        try:
            if rate_limit:
                await rate_limit.acquire(self.wait_on_rate_limit)
            try:
                response = await self._session.request(
                    method=method,
                    url=self._base_url / path.lstrip('/'),
                    raise_for_status=True,
                    **kwargs
                )
                return await response.json()
            except ClientResponseError as e:
                if e.status >= 500:
                    raise TinkoffInvestmentsUnavailableError from None
                elif e.status == 401:
                    raise TinkoffInvestmentsUnauthorizedError from None
                elif e.status == 429:
                    raise TinkoffInvestmentsTooManyRequestsError from None
                else:
                    raise
        except asyncio.TimeoutError:
            raise TinkoffInvestmentsTimeoutError from None
        except RateLimitReached:
            raise TinkoffInvestmentsTooManyRequestsError from None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


__all__ = [
    'TinkoffInvestmentsRESTClient'
]
