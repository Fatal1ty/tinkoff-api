from typing import List

from tinkoff.investments.api.base import BaseTinkoffInvestmentsAPI
from tinkoff.investments.model.user.accounts import UserAccount, UserAccounts


class UserAPI(BaseTinkoffInvestmentsAPI):
    async def get_accounts(self) -> List[UserAccount]:
        payload = await self._request(
            method="GET",
            path="/user/accounts",
        )
        return UserAccounts.from_dict(payload).accounts  # type: ignore
