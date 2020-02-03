from typing import NoReturn

from tinkoff.base import BaseClient
from tinkoff.investments.api import MarketAPI

from tinkoff.investments.client.environments import Environment, EnvironmentURL


class TinkoffInvestmentsRESTClient(BaseClient):
    def __init__(self, token, environment=Environment.PRODUCTION):
        # type: (str, Environment) -> NoReturn
        super(TinkoffInvestmentsRESTClient, self).__init__(
            base_url=EnvironmentURL[environment],
            headers={
                'authorization': f'Bearer {token}'
            }
        )
        self.market = MarketAPI(self)
