import copy
import logging
from typing import TYPE_CHECKING

import asyncio_atexit
from aiohttp import ClientSession

from .ratelimit_manager import RatelimitManager
from settings import __version__, API_KEY, BASE_URL, TIMEOUT

logger = logging.getLogger("vindicator.request")

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class RequestBase:

    def __init__(self) -> None:
        self.ratelimit_manager = RatelimitManager()

    async def start(self) -> None:
        headers = {
            "User-Agent": f"Vindicator/{__version__}",
            "Content-Type": "application/json"
        }

        if API_KEY is not None:
            headers["apikey"] = API_KEY

        self._session = ClientSession(headers=headers)
        asyncio_atexit.register(self._close)

    async def _close(self) -> 'ClientResponse':
        return await self._session.close()

    async def get(self, url_parameters: str, ratelimit_manager: RatelimitManager) -> dict:
        url = BASE_URL + url_parameters

        await ratelimit_manager.limit()
        response = await self._session.get(url, timeout=TIMEOUT)
        ratelimit_manager.update(response.headers)

        if 200 <= response.status < 400:
            return response
        else:
            raise Exception(f"Error {response.status} - {response.reason}")


class Request(RequestBase):

    def __init__(self) -> None:
        super().__init__()
        self.guild_rlm = RatelimitManager()
        self.online_rlm = RatelimitManager()
        self.player_rlm = RatelimitManager()

    async def get_guild_response(self, guild_name: str, is_prefix: bool = False) -> 'ClientResponse':
        url_parameters = f"guild/{'prefix/' if is_prefix else ''}{guild_name}"
        ret = await self.get(url_parameters, self.guild_rlm)
        return ret

    async def get_online_player_response(self) -> 'ClientResponse':
        url_parameters = "player"
        ret = await self.get(url_parameters, self.online_rlm)
        return ret

    async def get_player_response(self, username_or_uuid: str) -> 'ClientResponse':
        url_parameters = f"player/{username_or_uuid}?fullResult=True"
        ret = await self.get(url_parameters, self.player_rlm)
        return ret
