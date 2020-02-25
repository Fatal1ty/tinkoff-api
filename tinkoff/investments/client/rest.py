from typing import Any, Dict, Optional

from tinkoff.base import BaseHTTPClient, RateLimiter
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
    TinkoffInvestmentsUnauthorizedError, TinkoffInvestmentsTooManyRequestsError
)


class TinkoffInvestmentsRESTClient(BaseHTTPClient):
    def __init__(
            self,
            token: str,
            environment: Environment = Environment.PRODUCTION,
            timeout: Optional[float] = 5,
            rate_limit: Optional[RateLimiter] = RateLimiter(rate=120, period=60)
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
        self.rate_limit = rate_limit

    async def _request(self, method, path, **kwargs):
        # type: (str, str, Any) -> Dict[Any, Any]
        if self.rate_limit:
            await self.rate_limit.acquire()
        response = await self._session.request(
            method=method,
            url=self._base_url / path.lstrip('/'),
            **kwargs
        )
        if response.status == 401:
            raise TinkoffInvestmentsUnauthorizedError
        elif response.status == 429:
            raise TinkoffInvestmentsTooManyRequestsError
        else:
            # TODO: ловить другие исключения, если в ответе не json
            return await response.json()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
