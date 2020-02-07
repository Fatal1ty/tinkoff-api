from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.base import Currency, FigiName
from tinkoff.investments.model.sandbox import (
    SandboxAccountRegisterRequest,
    SandboxAccount,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
)
from tinkoff.investments.model.user.accounts import (
    BrokerAccountType,
    BrokerAccountID,
)


class SandboxAccountCurrenciesAPI(BaseTinkoffInvestmentsAPI):
    async def set_balance(self, broker_account_id, currency, balance):
        # type: (BrokerAccountID, Currency, float) -> None
        await self._request(
            method='POST',
            path='/sandbox/currencies/balance',
            params={
                'brokerAccountId': broker_account_id
            },
            json=SandboxSetCurrencyBalanceRequest(
                currency=currency,
                balance=balance
            ).to_dict()
        )


class SandboxAccountPositionsAPI(BaseTinkoffInvestmentsAPI):
    async def set_balance(self, broker_account_id, figi, balance):
        # type: (BrokerAccountID, FigiName, float) -> None
        await self._request(
            method='POST',
            path='/sandbox/positions/balance',
            params={
                'brokerAccountId': broker_account_id
            },
            json=SandboxSetPositionBalanceRequest(
                figi=figi,
                balance=balance
            ).to_dict()
        )


class SandboxAccountsAPI(BaseTinkoffInvestmentsAPI):
    def __init__(self, *args, **kwargs):
        super(SandboxAccountsAPI, self).__init__(*args, **kwargs)
        self.currencies = SandboxAccountCurrenciesAPI(*args, **kwargs)
        self.positions = SandboxAccountPositionsAPI(*args, **kwargs)

    async def register(self, broker_account_type=BrokerAccountType.TINKOFF):
        # type: (BrokerAccountType) -> SandboxAccount
        payload = await self._request(
            method='POST',
            path='/sandbox/register',
            json=SandboxAccountRegisterRequest(
                brokerAccountType=broker_account_type
            ).to_dict(),
        )
        return SandboxAccount.from_dict(payload)

    async def remove(self, broker_account_id: BrokerAccountID):
        await self._request(
            method='POST',
            path='/sandbox/remove',
            params={
                'brokerAccountId': broker_account_id
            }
        )

    async def clear(self, broker_account_id: BrokerAccountID):
        await self._request(
            method='POST',
            path='/sandbox/clear',
            params={
                'brokerAccountId': broker_account_id
            }
        )


class SandboxAPI(BaseTinkoffInvestmentsAPI):
    def __init__(self, *args, **kwargs):
        super(SandboxAPI, self).__init__(*args, **kwargs)
        self.accounts = SandboxAccountsAPI(*args, **kwargs)
