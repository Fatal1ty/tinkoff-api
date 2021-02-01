import asyncio
import time
from collections import deque
from typing import Deque, Dict, Optional

import aiohttp
from yarl import URL


class BaseHTTPClient:
    def __init__(self, base_url, headers=None, timeout=None):
        # type: (URL, Optional[Dict[str, str]], Optional[float]) -> None
        self._base_url = base_url
        self.__headers = headers
        self.__timeout = timeout
        self.__session = None  # type: Optional[aiohttp.ClientSession]

        self._closed = False

    @property
    def _session(self):
        if not self.__session:
            self.__session = aiohttp.ClientSession(
                headers=self.__headers,
                timeout=aiohttp.ClientTimeout(total=self.__timeout),
            )
        return self.__session

    async def close(self):
        self._closed = True
        await self._session.close()
        self.__session = None

    @property
    def closed(self):
        return self._closed


# noinspection PyPep8Naming
class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class RateLimitReached(Exception):
    pass


class RateLimiter:
    def __init__(self, rate: int, period: float):
        self.rate = rate
        self.period = period
        self.request_times: Deque[float] = deque()

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def acquire(self, blocking=True):
        while not self._try_to_acquire():
            if not blocking:
                raise RateLimitReached
            await asyncio.sleep(0.25)

    def _try_to_acquire(self):
        now = time.monotonic()
        while self.request_times:
            if now - self.request_times[0] > self.period:
                self.request_times.popleft()
            else:
                break
        if len(self.request_times) < self.rate:
            self.request_times.append(now)
            return True
        else:
            return False


__all__ = [
    "BaseHTTPClient",
    "classproperty",
    "RateLimiter",
    "RateLimitReached",
]
