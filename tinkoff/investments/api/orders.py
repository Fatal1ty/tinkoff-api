from typing import List

from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.user.accounts import BrokerAccountID
from tinkoff.investments.model.orders import (
    Order,
    OrderID,
    PlacedLimitOrder,
    LimitOrderRequest,
    PlacedMarketOrder,
    MarketOrderRequest,
)
from tinkoff.investments.model.operations import OperationType
from tinkoff.investments.model.base import FigiName


class OrdersAPI(BaseTinkoffInvestmentsAPI):
    async def get(self, broker_account_id=None):
        # type: (BrokerAccountID) -> List[Order]

        if broker_account_id is not None:
            params = {'brokerAccountId': broker_account_id}
        else:
            params = {}

        payload = await self._request(
            method='GET',
            path='/orders',
            params=params
        )
        return [Order.from_dict(obj) for obj in payload]

    async def create_limit_order(
            self,
            figi: FigiName,
            lots: int,
            operation: OperationType,
            price: float,
            broker_account_id: BrokerAccountID = None
    ) -> PlacedLimitOrder:

        params = {
            'figi': figi
        }
        if broker_account_id is not None:
            params['brokerAccountId'] = broker_account_id

        payload = await self._request(
            method='POST',
            path='/orders/limit-order',
            params=params,
            json=LimitOrderRequest(
                lots=lots,
                operation=operation,
                price=price,
            ).to_dict()
        )
        return PlacedLimitOrder.from_dict(payload)

    async def create_market_order(
            self,
            figi: FigiName,
            lots: int,
            operation: OperationType,
            broker_account_id: BrokerAccountID = None
    ) -> PlacedMarketOrder:

        params = {
            'figi': figi
        }
        if broker_account_id is not None:
            params['brokerAccountId'] = broker_account_id

        payload = await self._request(
            method='POST',
            path='/orders/market-order',
            params=params,
            json=MarketOrderRequest(
                lots=lots,
                operation=operation,
            ).to_dict()
        )
        return PlacedMarketOrder.from_dict(payload)

    async def cancel(self, order_id, broker_account_id=None):
        # type: (OrderID, BrokerAccountID) -> None

        params = {
            'orderId': order_id
        }
        if broker_account_id is not None:
            params['brokerAccountId'] = broker_account_id

        await self._request(
            method='POST',
            path='/orders/cancel',
            params=params,
        )
