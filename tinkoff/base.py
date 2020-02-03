from typing import Optional, Dict, Any

import aiohttp
from yarl import URL


class BaseClient:
    def __init__(self, base_url: URL, headers: Optional[Dict[str, str]] = None):
        self._base_url = base_url
        self._session = aiohttp.ClientSession(headers=headers)

    async def _request(self, method, path, **kwargs):
        # type: (str, str, Any) -> Dict[Any, Any]
        response = await self._session.request(
            method=method,
            url=self._base_url / path.lstrip('/'),
            **kwargs
        )
        return await response.json()

    async def close(self):
        await self._session.close()
