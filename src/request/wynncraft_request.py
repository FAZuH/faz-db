import asyncio
from typing import TYPE_CHECKING, Any, Coroutine, Iterable, List, Tuple, TypeAlias, Union

from aiohttp import ClientResponse

from .ratelimit import Ratelimit
from .request_base import RequestBase
from constants import __version__

if TYPE_CHECKING:
    from uuid import UUID

    from objects.wynncraft_response import GuildList, GuildStats, OnlinePlayerList, PlayerStats

ReturnGather: TypeAlias = Union[BaseException, ClientResponse]
tReturnGather: TypeAlias = Tuple[ReturnGather]


class WynncraftRequest(RequestBase):

    _guild_rl: Ratelimit = Ratelimit(300, 120)
    _online_rl: Ratelimit = Ratelimit(300, 120)
    _player_rlm: Ratelimit = Ratelimit(300, 120)

    def __init__(self) -> None:
        super().__init__("https://api.wynncraft.com")

    # Guild Stats
    def get_guild_stats_coro(self, guild_name: str, is_prefix: bool = False) -> Coroutine[Any, Any, ClientResponse]:
        url_parameters: str = f"guild/{'prefix/' if is_prefix else ''}{guild_name}"
        return self.get(url_parameters, WynncraftRequest._guild_rl)

    async def get_guild_stats_json(self, guild_name: str, is_prefix: bool = False) -> Union[BaseException, "GuildStats"]:
        response: ReturnGather = await self.get_guild_stats_response(guild_name, is_prefix)
        return await response.json() if isinstance(response, ClientResponse) else response

    async def get_guild_stats_response(self, guild_name: str, is_prefix: bool = False) -> ClientResponse:
        return await self.get_guild_stats_coro(guild_name, is_prefix)

    async def get_many_guild_stats_response(self, guild_names: Iterable[str], is_prefix: bool = False) -> Tuple[List[BaseException], List[ClientResponse]]:
        coros: List[Coroutine[Any, Any, ReturnGather]] = [self.get_guild_stats_coro(g, is_prefix) for g in guild_names]
        results: List[ReturnGather] = await asyncio.gather(*coros, return_exceptions=True)
        exceptions = []
        responses = []
        for result in results:
            if isinstance(result, BaseException):
                exceptions.append(result)
            elif isinstance(result, ClientResponse):
                responses.append(result)
        return exceptions, responses

    async def get_many_guild_stats_json(self, guild_names: Iterable[str], is_prefix: bool = False) -> Tuple[List[BaseException], List["GuildStats"]]:
        exceptions: List[BaseException]
        responses: List[ClientResponse]
        exceptions, responses = await self.get_many_guild_stats_response(guild_names)
        coros: List[Coroutine[Any, Any, dict]] = [r.json() for r in responses]
        guild_stats: List["GuildStats"] = await asyncio.gather(*coros, return_exceptions=True)
        return exceptions, guild_stats

    # Online Players
    async def get_online_player_response(self) -> ReturnGather:
        url_parameters: str = "player"
        return await self.get(url_parameters, WynncraftRequest._online_rl)

    async def get_online_player_json(self, json_response: bool = True) -> Union[BaseException, "OnlinePlayerList"]:
        response: ReturnGather = await self.get_online_player_response()
        return await response.json() if isinstance(response, ClientResponse) else response

    # Player Stats
    def get_player_stats_coro(self, username_or_uuid: Union[str, "UUID"]) -> Coroutine[Any, Any, ClientResponse]:
        url_parameters: str = f"v3/player/{username_or_uuid}?fullResult=True"
        return self.get(url_parameters, WynncraftRequest._player_rlm)

    async def get_player_stats_response(self, username_or_uuid: Union[str, "UUID"]) -> ClientResponse:
        return await self.get_player_stats_coro(username_or_uuid)

    async def get_player_stats_json(self, username_or_uuid: Union[str, "UUID"]) -> Union[BaseException, "PlayerStats"]:
        response: ReturnGather = await self.get_player_stats_response(username_or_uuid)
        return await response.json() if isinstance(response, ClientResponse) else response

    async def get_many_player_stats_response(self, usernames_or_uuids: Iterable[Union[str, "UUID"]]) -> Tuple[List[BaseException], List[ClientResponse]]:
        coros: List[Coroutine] = [self.get_player_stats_coro(u) for u in usernames_or_uuids]
        results: List[ReturnGather] = await asyncio.gather(*coros, return_exceptions=True)
        exceptions = []
        responses = []
        for result in results:
            if isinstance(result, BaseException):
                exceptions.append(result)
            elif isinstance(result, ClientResponse):
                responses.append(result)
        return exceptions, responses

    async def get_many_player_stats_json(self, usernames_or_uuids: Iterable[Union[str, "UUID"]]) -> Tuple[List[BaseException], List["PlayerStats"]]:
        exceptions: List[BaseException]
        responses: List[ClientResponse]
        exceptions, responses = await self.get_many_player_stats_response(usernames_or_uuids)
        coros: List[Coroutine] = [r.json() for r in responses]
        player_stats: List["PlayerStats"] = await asyncio.gather(*coros, return_exceptions=True)
        return exceptions, player_stats

class GuildListRequest(RequestBase):

    _ttl: int = 3600
    async def get_guild_list_response(self) -> ClientResponse:
        url_parameters: str = "guild/list/guild"
        return await self.get(url_parameters, WynncraftRequest._guild_rl)

    async def get_guild_list_json(self) -> Union[BaseException, "GuildList"]:
        response: ReturnGather = await self.get_guild_list_response()
        return await response.json() if isinstance(response, ClientResponse) else response
    pass

class GuildStatsRequest:
    pass

class OnlinePlayersRequest:
    pass

class
