from __future__ import annotations
from asyncio import gather
from typing import TYPE_CHECKING, Any, Coroutine, Iterable, List, Tuple, Union

from aiohttp import ClientResponse, ClientSession

from vindicator import (
    Ratelimit,
    RequestManager,
)
from vindicator.constants import __version__

if TYPE_CHECKING:
    from vindicator.types import *


class WynncraftRequest:

    _rm: RequestManager = RequestManager("https://api.wynncraft.com", ratelimit=Ratelimit(180, 60))

    # Online Players
    @classmethod
    async def get_online_uuids(cls) -> OnlinePlayerList:
        async with cls._rm.session as s:
            return await (await cls._rm.get("/v3/player?identifier=uuid", s, retries=3, retry_on_exc=True)).json()

    # Player Stats
    @classmethod
    def get_player_stats_coro(
        cls,
        session: ClientSession,
        username_or_uuid: Union[str, UUID]
    ) -> Coroutine[Any, Any, ClientResponse]:
        return cls._rm.get(f"/v3/player/{username_or_uuid}?fullResult=True", session, retries=3, retry_on_exc=True)

    @classmethod
    async def get_many_player_stats_response(
        cls,
        session: ClientSession,
        usernames_or_uuids: Iterable[Union[str, UUID]]
    ) -> Tuple[List[BaseException], List[ClientResponse]]:
        coros: List[Coroutine] = [cls.get_player_stats_coro(session, u) for u in usernames_or_uuids]
        excs = []
        resps = []
        for res in (await gather(*coros, return_exceptions=True)):
            if isinstance(res, BaseException):
                excs.append(res)
            elif isinstance(res, ClientResponse):
                resps.append(res)
        return excs, resps

    # Guild Stats
    @classmethod
    def get_guild_stats_coro(
        cls,
        session: ClientSession,
        name_or_prefix: str,
        is_prefix: bool = False
    ) -> Coroutine[Any, Any, ClientResponse]:
        return cls._rm.get(f"/v3/guild/{'prefix/' if is_prefix else ''}{name_or_prefix}", session, retries=3, retry_on_exc=True)

    @classmethod
    async def get_many_guild_stats_response(
        cls,
        session: ClientSession,
        names_or_prefixes: Iterable[str],
        is_prefix: bool = False
    ) -> Tuple[List[BaseException], List[ClientResponse]]:
        coros: List[Coroutine] = [cls.get_guild_stats_coro(session, u, is_prefix) for u in names_or_prefixes]
        excs = []
        resps = []
        for res in (await gather(*coros, return_exceptions=True)):
            if isinstance(res, BaseException):
                excs.append(res)
            elif isinstance(res, ClientResponse):
                resps.append(res)
        return excs, resps

    # # Guild Stats
    # def get_guild_stats_coro(self, guild_name: str, is_prefix: bool = False) -> Coroutine[Any, Any, ClientResponse]:
    #     url_parameters: str = f"/guild/{'prefix/' if is_prefix else ''}{guild_name}"
    #     return self.get(url_parameters, WynncraftRequest._wynncraft_rl)

    # async def get_guild_stats_response(self, guild_name: str, is_prefix: bool = False) -> ClientResponse:
    #     return await self.get_guild_stats_coro(guild_name, is_prefix)

    # async def get_guild_stats_json(self, guild_name: str, is_prefix: bool = False) -> Union[BaseException, "GuildStats"]:
    #     response: ReturnGather = await self.get_guild_stats_response(guild_name, is_prefix)
    #     return await response.json() if isinstance(response, ClientResponse) else response

    # async def get_many_guild_stats_response(self, guild_names: Iterable[str], is_prefix: bool = False) -> Tuple[List[BaseException], List[ClientResponse]]:
    #     coros: List[Coroutine[Any, Any, ReturnGather]] = [self.get_guild_stats_coro(g, is_prefix) for g in guild_names]
    #     results: List[ReturnGather] = await asyncio.gather(*coros, return_exceptions=True)
    #     exceptions = []
    #     responses = []
    #     for result in results:
    #         if isinstance(result, BaseException):
    #             exceptions.append(result)
    #         elif isinstance(result, ClientResponse):
    #             responses.append(result)
    #     return exceptions, responses

    # async def get_many_guild_stats_json(self, guild_names: Iterable[str], is_prefix: bool = False) -> Tuple[List[BaseException], List["GuildStats"]]:
    #     exceptions: List[BaseException]
    #     responses: List[ClientResponse]
    #     exceptions, responses = await self.get_many_guild_stats_response(guild_names)
    #     coros: List[Coroutine[Any, Any, dict]] = [r.json() for r in responses]
    #     guild_stats: List["GuildStats"] = await asyncio.gather(*coros, return_exceptions=True)  # type: ignore
    #     return exceptions, guild_stats

    # @staticmethod
    # async def get_player_stats(username_or_uuid: Union[str, "UUID"]) -> "PlayerStats":
    #     async with WynncraftRequest._rm.session as s:
    #         return await (await WynncraftRequest.get_player_stats_coro(s, username_or_uuid)).json()

    # async def get_player_stats_response(self, username_or_uuid: Union[str, "UUID"]) -> ClientResponse:
    #     return await self.get_player_stats_coro(username_or_uuid)

    # async def get_player_stats_json(self, username_or_uuid: Union[str, "UUID"]) -> Union[BaseException, "PlayerStats"]:
    #     response: ReturnGather = await self.get_player_stats_response(username_or_uuid)
    #     return await response.json() if isinstance(response, ClientResponse) else response

    # async def get_many_player_stats_json(self, usernames_or_uuids: Iterable[Union[str, "UUID"]]) -> Tuple[List[BaseException], List["PlayerStats"]]:
    #     exceptions: List[BaseException]
    #     responses: List[ClientResponse]
    #     exceptions, responses = await self.get_many_player_stats_response(usernames_or_uuids)
    #     coros: List[Coroutine] = [r.json() for r in responses]
    #     player_stats: List["PlayerStats"] = await asyncio.gather(*coros, return_exceptions=True)
    #     return exceptions, player_stats
