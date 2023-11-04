import asyncio
from typing import TYPE_CHECKING, Any, Coroutine, Iterable, List, Union
from time import perf_counter # TODO: REMOVE THIS
import asyncio_atexit

from .ratelimit_manager import RatelimitManager
from .api_request_base import APIRequestBase
from settings import __version__

# logger = logging.getLogger("vindicator.request")

if TYPE_CHECKING:
    from uuid import UUID

    from aiohttp import ClientResponse

    from objects.wynncraft_response import GuildList, GuildStats, OnlinePlayerList, PlayerStats

BASE_URL: str = "https://api.wynncraft.com/v3/"
TIMEOUT: int = 60


class WynncraftAPIRequest:

    _guild_rlm = RatelimitManager(300, 120)
    _online_rlm = RatelimitManager(300, 120)
    _player_rlm = RatelimitManager(300, 120)
    _session = APIRequestBase(BASE_URL, timeout=TIMEOUT)

    @classmethod
    async def ainit(cls) -> None:
        await cls._session.start()
        asyncio_atexit.register(cls._session._close)

    @classmethod
    async def get_guild_list_response(cls) -> "ClientResponse":
        url_parameters: str = "guild/list/guild"
        return await cls._session.get(url_parameters, ratelimit_manager=cls._guild_rlm)

    @classmethod
    async def get_guild_list_json(cls) -> "GuildList":
        response: "ClientResponse" = await cls.get_guild_list_response()
        return await response.json()

    @classmethod
    async def get_guild_stats_response(cls, guild_name: str, is_prefix: bool = False) -> "ClientResponse":
        url_parameters: str = f"guild/{'prefix/' if is_prefix else ''}{guild_name}"
        return await cls._session.get(url_parameters, ratelimit_manager=cls._guild_rlm)

    @classmethod
    async def get_guild_stats_json(cls, guild_name: str, is_prefix: bool = False) -> "GuildStats":
        response: "ClientResponse" = await cls.get_guild_stats_response(guild_name, is_prefix)
        return await response.json()

    @classmethod
    async def get_many_guild_stats_response(cls, guild_names: Iterable[str], is_prefix: bool = False) -> List["ClientResponse"]:
        coros: List[Coroutine[Any, Any, "ClientResponse"]] = [cls.get_guild_stats_response(g, is_prefix) for g in guild_names]
        t0 = perf_counter()
        results: List["ClientResponse"] = await asyncio.gather(*coros, return_exceptions=True)
        print((perf_counter() - t0)/25)
        return [result for result in results if not isinstance(result, Exception)]

    @classmethod
    async def get_many_guild_stats_json(cls, guild_names: Iterable[str], is_prefix: bool = False) -> List["GuildStats"]:
        responses: List["ClientResponse"] = await cls.get_many_guild_stats_response(guild_names, is_prefix)
        coros: List[Coroutine[Any, Any, dict]] = [r.json() for r in responses]
        results: List["GuildStats"] = await asyncio.gather(*coros, return_exceptions=True)
        return [result for result in results if not isinstance(result, Exception)]

    @classmethod
    async def get_online_player_response(cls) -> "ClientResponse":
        url_parameters: str = "player"
        return await cls._session.get(url_parameters, ratelimit_manager=cls._online_rlm)

    @classmethod
    async def get_online_player_json(cls, json_response: bool = True) -> "OnlinePlayerList":
        response: "ClientResponse" = await cls.get_online_player_response()
        return await response.json()

    @classmethod
    async def get_player_stats_response(cls, username_or_uuid: Union[str, "UUID"]) -> "ClientResponse":
        url_parameters: str = f"player/{username_or_uuid}?fullResult=True"
        return await cls._session.get(url_parameters, ratelimit_manager=cls._player_rlm)

    @classmethod
    async def get_player_stats_json(cls, username_or_uuid: Union[str, "UUID"]) -> "PlayerStats":
        response: "ClientResponse" = await cls.get_player_stats_response(username_or_uuid)
        return await response.json()

    @classmethod
    async def get_many_player_stats_response(cls, usernames_or_uuids: Iterable[Union[str, "UUID"]]) -> List["ClientResponse"]:
        coros: List[Coroutine[Any, Any, "ClientResponse"]] = [cls.get_player_stats_response(u) for u in usernames_or_uuids]
        results: List["ClientResponse"] = await asyncio.gather(*coros, return_exceptions=True)
        return [result for result in results if not isinstance(result, Exception)]

    @classmethod
    async def get_many_player_stats_json(cls, usernames_or_uuids: Iterable[Union[str, "UUID"]]) -> List["PlayerStats"]:
        responses: List["ClientResponse"] = await cls.get_many_player_stats_response(usernames_or_uuids)
        coros: List[Coroutine[Any, Any, "PlayerStats"]] = [r.json() for r in responses]
        results: List["PlayerStats"] = await asyncio.gather(*coros, return_exceptions=True)
        return [result for result in results if not isinstance(result, Exception)]
