from datetime import datetime, timezone
from typing import List

from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.base import FigiName
from tinkoff.investments.model.user.accounts import BrokerAccountID
from tinkoff.investments.model.operations import Operation, Operations


class OperationsAPI(BaseTinkoffInvestmentsAPI):
    async def get(
            self,
            dt_from: datetime,
            dt_to: datetime,
            figi: FigiName = None,
            broker_account_id: BrokerAccountID = None
    ) -> List[Operation]:

        if not dt_from.tzinfo:
            dt_from = dt_from.replace(tzinfo=timezone.utc)
        if not dt_to.tzinfo:
            dt_to = dt_to.replace(tzinfo=timezone.utc)
        params = {
            'from': dt_from.isoformat(),
            'to': dt_to.isoformat(),
        }
        if figi is not None:
            params['figi'] = figi
        if broker_account_id is not None:
            params['brokerAccountId'] = broker_account_id

        payload = await self._request(
            method='GET',
            path='/operations',
            params=params,
        )
        return Operations.from_dict(payload).operations
