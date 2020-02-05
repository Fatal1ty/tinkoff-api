from typing import Optional, Dict, Any

import aiohttp
from yarl import URL


class BaseHTTPClient:
    def __init__(self, base_url: URL, headers: Optional[Dict[str, str]] = None):
        self._base_url = base_url
        self.__headers = headers
        self.__session = None  # type: aiohttp.ClientSession

    @property
    def _session(self):
        if not self.__session:
            self.__session = aiohttp.ClientSession(headers=self.__headers)
        return self.__session

    async def close(self):
        await self._session.close()
