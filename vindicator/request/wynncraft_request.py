from __future__ import annotations
from asyncio import gather

from vindicator import Ratelimit, RequestManager, ResponseSet
from vindicator.constants import *
from vindicator.typehints import *


class WynncraftRequest:

    _rm: RequestManager = RequestManager("https://api.wynncraft.com", ratelimit=Ratelimit(180, 60))


    def __init__(self) -> None:
        self._session = WynncraftRequest._rm.create_session()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: ExcTypeT, exc: ExcT, tb: TbT) -> None:
        await self._session.close()


    async def get_online_uuids(self) -> ResponseSet[OnlinePlayerList, Headers]:
        return await WynncraftRequest._rm.get_as_resultset(
                "/v3/player?identifier=uuid",
                self._session,
                retries=3,
                retry_on_exc=True
        )

    # Player Stats
    def get_player_stats_coro(self, username_or_uuid: Union[str, UUID]) -> Coro[ResponseSet[PlayerStats, Headers]]:
        return WynncraftRequest._rm.get_as_resultset(
                f"/v3/player/{username_or_uuid}?fullResult=True",
                self._session,
                retries=3,
                retry_on_exc=True
        )

    async def get_many_player_stats(
        self,
        usernames_or_uuids: Iterable[Union[str, UUID]]
    ) -> Tuple[List[BaseException], List[ResponseSet[PlayerStats, Headers]]]:
        coros: List[Coro[ResponseSet[PlayerStats, Headers]]] = [self.get_player_stats_coro(u) for u in usernames_or_uuids]
        excs: List[BaseException] = []
        ress: List[ResponseSet[PlayerStats, Headers]] = []
        for res in (await gather(*coros, return_exceptions=True)):
            if isinstance(res, BaseException):
                excs.append(res)
            elif isinstance(res, ResponseSet):
                ress.append(res)
        return excs, ress

    # Guild Stats
    def get_guild_stats_coro(self, name_or_prefix: str, is_prefix: bool = False) -> Coro[ResponseSet[GuildStats, Headers]]:
        return WynncraftRequest._rm.get_as_resultset(
                f"/v3/guild/{'prefix/' if is_prefix else ''}{name_or_prefix}",
                self._session,
                retries=3,
                retry_on_exc=True
        )

    async def get_many_guild_stats(
        self,
        names_or_prefixes: Iterable[str],
        is_prefix: bool = False
    ) -> Tuple[List[BaseException], List[ResponseSet[GuildStats, Headers]]]:
        coros: List[Coro[ResponseSet[GuildStats, Headers]]] = [self.get_guild_stats_coro(u, is_prefix) for u in names_or_prefixes]
        excs: List[BaseException] = []
        ress: List[ResponseSet[GuildStats, Headers]] = []
        for res in (await gather(*coros, return_exceptions=True)):
            if isinstance(res, BaseException):
                excs.append(res)
            elif isinstance(res, ResponseSet):
                ress.append(res)
        return excs, ress
