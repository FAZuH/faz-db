from datetime import datetime
from dateutil.tz import tzutc
from typing import TYPE_CHECKING, Union

import asyncio_atexit

from .ratelimit_manager import RatelimitManager
from .request_base import RequestBase
from settings import __version__

# logger = logging.getLogger("vindicator.request")

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from typeddict.wynncraft_response import OnlinePlayerList, PlayerStats

BASE_URL: str = "https://api.wynncraft.com/v3/"
TIMEOUT: int = 60


class RequestWynncraft:
    _guild_rlm = RatelimitManager(300, 60)
    _online_rlm = RatelimitManager(300, 60)
    _player_rlm = RatelimitManager(300, 60)
    _session = RequestBase(BASE_URL, timeout=TIMEOUT)

    @classmethod
    async def ainit(cls) -> None:
        await cls._session.start()
        asyncio_atexit.register(cls._session._close())

    async def get_guild_stats(self, guild_name: str, is_prefix: bool = False, json_response: bool = True) -> dict:
        url_parameters = f"guild/{'prefix/' if is_prefix else ''}{guild_name}"
        ret = await self.session.get(url_parameters, ratelimit_manager=self.guild_rlm)
        return await ret.json() if json_response else ret

    async def get_online_player_list(self, json_response: bool = True) -> Union["ClientResponse", "OnlinePlayerList"]:
        url_parameters = "player"
        ret = await self.session.get(url_parameters, ratelimit_manager=self.online_rlm)
        return await ret.json() if json_response else ret

    async def get_player_stats(self, username_or_uuid: str, json_response: bool = True) -> Union["ClientResponse", "PlayerStats"]:
        url_parameters = f"player/{username_or_uuid}?fullResult=True"
        ret = await self.session.get(url_parameters, ratelimit_manager=self.player_rlm)
        return await ret.json() if json_response else ret

    @property
    def guild_rlm(self) -> RatelimitManager:
        return RequestWynncraft._guild_rlm

    @property
    def online_rlm(self) -> RatelimitManager:
        return RequestWynncraft._online_rlm

    @property
    def player_rlm(self) -> RatelimitManager:
        return RequestWynncraft._player_rlm

    @property
    def session(self) -> RequestBase:
        return RequestWynncraft._session


class WynncraftResponseUtils:

    @staticmethod
    def parse_datestr(datestr: str) -> int:
        return int(datetime.strptime(datestr, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tzutc()).timestamp())
