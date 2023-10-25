from typing import TYPE_CHECKING

from aiohttp import ClientSession
import asyncio_atexit

from settings import __version__

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from .ratelimit_manager import RatelimitManager


class RequestBase:

    def __init__(self, base_url: str, api_key: str = None, timeout: int = 120) -> None:
        self.api_key: str = api_key
        self.base_url: str = base_url
        self.timeout: int = timeout
        self._client_session: ClientSession = None

    async def start(self) -> None:
        headers = {
            "User-Agent": f"Vindicator/{__version__}",
            "Content-Type": "application/json"
        }

        if self.api_key is not None:
            headers["apikey"] = self.api_key

        self._client_session = ClientSession(headers=headers)
        asyncio_atexit.register(self._close)

    async def _close(self) -> None:
        await self._client_session.close()

    async def get(self, url_parameters: str, ratelimit_manager: "RatelimitManager" = None) -> 'ClientResponse':
        url = self.base_url + url_parameters

        if ratelimit_manager is None:
            response = await self._client_session.get(url, timeout=self.timeout)
        else:
            await ratelimit_manager.limit()
            response = await self._client_session.get(url, timeout=self.timeout)
            ratelimit_manager.update(response.headers)

        if 200 <= response.status < 400:
            return response
        elif response.status == 429 and ratelimit_manager:
            ratelimit_manager.ratelimited()
            await self.get(url_parameters, ratelimit_manager)
        else:
            raise Exception(f"Error {response.status} - {response.reason}")
