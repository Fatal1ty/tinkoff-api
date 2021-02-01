from typing import Any, Dict, List, Union

from tinkoff.base import RateLimiter
from tinkoff.investments.client.exceptions import TinkoffInvestmentsAPIError
from tinkoff.investments.model.base import Error
from tinkoff.investments.model.response import TinkoffInvestmentsAPIResponse


class BaseTinkoffInvestmentsAPI:
    def __init__(self, client):
        self._client = client
        self._default_rate_limit = self._get_default_rate_limiter()
        self._path_rate_limits = self._get_path_rate_limiters()

    def _get_default_rate_limiter(self) -> RateLimiter:
        return RateLimiter(rate=120, period=60)

    def _get_path_rate_limiters(self) -> Dict[str, RateLimiter]:
        return {}

    async def _request(self, method, path, **kwargs):
        # type: (str, str, Any) -> Union[Dict[Any, Any], List[Any]]
        rate_limit = self._path_rate_limits.get(path, self._default_rate_limit)
        # noinspection PyProtectedMember
        data = await self._client._request(method, path, rate_limit, **kwargs)
        response = TinkoffInvestmentsAPIResponse.from_dict(data)
        if response.is_successful():
            return response.payload
        else:
            raise TinkoffInvestmentsAPIError(
                tracking_id=response.trackingId,
                status=response.status,
                error=Error(
                    message=response.payload.get("message"),
                    code=response.payload.get("code"),
                ),
            )


__all__ = [
    "BaseTinkoffInvestmentsAPI",
]
