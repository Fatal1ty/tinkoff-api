from typing import Dict, List

from tinkoff.base import RateLimiter
from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.base import FigiName
from tinkoff.investments.model.operations import OperationType
from tinkoff.investments.model.orders import (
    LimitOrderRequest,
    MarketOrderRequest,
    Order,
    OrderID,
    PlacedLimitOrder,
    PlacedMarketOrder,
)
from tinkoff.investments.model.user.accounts import BrokerAccountID


class OrdersAPI(BaseTinkoffInvestmentsAPI):
    def _get_default_rate_limiter(self) -> RateLimiter:
        return RateLimiter(rate=100, period=60)

    def _get_path_rate_limiters(self) -> Dict[str, RateLimiter]:
        return {
            "/orders": RateLimiter(rate=100, period=60),
            "/orders/limit-order": RateLimiter(rate=100, period=60),
            "/orders/market-order": RateLimiter(rate=100, period=60),
            "/orders/cancel": RateLimiter(rate=50, period=60),
        }

    async def get(self, broker_account_id=None):
        # type: (BrokerAccountID) -> List[Order]

        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}

        payload = await self._request(
            method="GET", path="/orders", params=params
        )
        return [Order.from_dict(obj) for obj in payload]

    async def create_limit_order(
        self,
        figi: FigiName,
        lots: int,
        operation: OperationType,
        price: float,
        broker_account_id: BrokerAccountID = None,
    ) -> PlacedLimitOrder:

        params = {"figi": figi}
        if broker_account_id is not None:
            params["brokerAccountId"] = broker_account_id

        payload = await self._request(
            method="POST",
            path="/orders/limit-order",
            params=params,
            json=LimitOrderRequest(
                lots=lots,
                operation=operation,
                price=price,
            ).to_dict(),
        )
        return PlacedLimitOrder.from_dict(payload)  # type: ignore

    async def create_market_order(
        self,
        figi: FigiName,
        lots: int,
        operation: OperationType,
        broker_account_id: BrokerAccountID = None,
    ) -> PlacedMarketOrder:

        params = {"figi": figi}
        if broker_account_id is not None:
            params["brokerAccountId"] = broker_account_id

        payload = await self._request(
            method="POST",
            path="/orders/market-order",
            params=params,
            json=MarketOrderRequest(
                lots=lots,
                operation=operation,
            ).to_dict(),
        )
        return PlacedMarketOrder.from_dict(payload)  # type: ignore

    async def cancel(self, order_id, broker_account_id=None):
        # type: (OrderID, BrokerAccountID) -> None

        params = {"orderId": order_id}
        if broker_account_id is not None:
            params["brokerAccountId"] = broker_account_id

        await self._request(
            method="POST",
            path="/orders/cancel",
            params=params,
        )
