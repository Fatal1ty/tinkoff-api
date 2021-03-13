from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.base import Currency, FigiName
from tinkoff.investments.model.sandbox import (
    SandboxAccount,
    SandboxAccountRegisterRequest,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
)
from tinkoff.investments.model.user.accounts import (
    BrokerAccountID,
    BrokerAccountType,
)


class SandboxAccountCurrenciesAPI(BaseTinkoffInvestmentsAPI):
    async def set_balance(self, currency, balance, broker_account_id=None):
        # type: (Currency, float, BrokerAccountID) -> None
        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}
        await self._request(
            method="POST",
            path="/sandbox/currencies/balance",
            params=params,
            json=SandboxSetCurrencyBalanceRequest(
                currency=currency, balance=balance
            ).to_dict(),
        )


class SandboxAccountPositionsAPI(BaseTinkoffInvestmentsAPI):
    async def set_balance(self, figi, balance, broker_account_id=None):
        # type: (FigiName, float, BrokerAccountID) -> None
        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}
        await self._request(
            method="POST",
            path="/sandbox/positions/balance",
            params=params,
            json=SandboxSetPositionBalanceRequest(
                figi=figi, balance=balance
            ).to_dict(),
        )


class SandboxAccountsAPI(BaseTinkoffInvestmentsAPI):
    def __init__(self, *args, **kwargs):
        super(SandboxAccountsAPI, self).__init__(*args, **kwargs)
        self.currencies = SandboxAccountCurrenciesAPI(*args, **kwargs)
        self.positions = SandboxAccountPositionsAPI(*args, **kwargs)

    async def register(self, broker_account_type=BrokerAccountType.TINKOFF):
        # type: (BrokerAccountType) -> SandboxAccount
        payload = await self._request(
            method="POST",
            path="/sandbox/register",
            json=SandboxAccountRegisterRequest(
                brokerAccountType=broker_account_type
            ).to_dict(),
        )
        return SandboxAccount.from_dict(payload)  # type: ignore

    async def remove(self, broker_account_id: BrokerAccountID = None):
        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}
        await self._request(
            method="POST",
            path="/sandbox/remove",
            params=params,
        )

    async def clear(self, broker_account_id: BrokerAccountID = None):
        if broker_account_id is not None:
            params = {"brokerAccountId": broker_account_id}
        else:
            params = {}
        await self._request(
            method="POST",
            path="/sandbox/clear",
            params=params,
        )


class SandboxAPI(BaseTinkoffInvestmentsAPI):
    def __init__(self, *args, **kwargs):
        super(SandboxAPI, self).__init__(*args, **kwargs)
        self.accounts = SandboxAccountsAPI(*args, **kwargs)
