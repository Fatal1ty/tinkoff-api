from typing import NoReturn, Any, Dict

from aiohttp import ClientResponseError

from tinkoff.base import BaseHTTPClient
from tinkoff.investments.api import MarketAPI
from tinkoff.investments.client.environments import Environment, EnvironmentURL
from tinkoff.investments.client.exceptions import (
    TinkoffInvestmentsUnauthorizedError,
)


class TinkoffInvestmentsRESTClient(BaseHTTPClient):
    def __init__(self, token, environment=Environment.PRODUCTION):
        # type: (str, Environment) -> NoReturn
        super(TinkoffInvestmentsRESTClient, self).__init__(
            base_url=EnvironmentURL[environment],
            headers={
                'authorization': f'Bearer {token}'
            }
        )
        self.market = MarketAPI(self)

    async def _request(self, method, path, **kwargs):
        # type: (str, str, Any) -> Dict[Any, Any]
        try:
            response = await self._session.request(
                method=method,
                url=self._base_url / path.lstrip('/'),
                raise_for_status=True,
                **kwargs
            )
            return await response.json()
        except ClientResponseError as e:
            if e.status == 401:
                raise TinkoffInvestmentsUnauthorizedError
