from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from kans import GuildResponse, PlayerResponse, PlayersResponse, TaskBase

if TYPE_CHECKING:
    from kans import (
        App,
        FetchGuildTask,
        FetchOnlineTask,
        FetchPlayerTask,
        RequestQueue,
    )


class FetchCoreTask(TaskBase):

    def __init__(
        self,
        app: App,
        fetch_guild: FetchGuildTask,
        fetch_online: FetchOnlineTask,
        fetch_player: FetchPlayerTask,
        request_queue: RequestQueue,
    ) -> None:
        self._app = app
        self._fetch_guild = fetch_guild
        self._fetch_online = fetch_online
        self._fetch_player = fetch_player
        self._request_queue = request_queue

        self._concurrent_request = 36
        self._event_loop = asyncio.new_event_loop()

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())

    async def _run(self) -> None:
        coros = tuple(item.coro_f(item.requestarg) for item in self._request_queue.getmany(self._concurrent_request))
        async with self._app.wynnapi:
            resps = await asyncio.gather(*coros, return_exceptions=True)

        self._app.logger.debug(f"Fetched {len(resps)} responses")
        for resp in resps:
            if isinstance(resp, Exception):
                # TODO: Log exception
                pass
            elif isinstance(resp, PlayerResponse):
                self._fetch_player.put_response(resp)
            elif isinstance(resp, PlayersResponse):
                self._fetch_online.put_response(resp)
            elif isinstance(resp, GuildResponse):
                self._fetch_guild.put_response(resp)

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def name(self) -> str:
        return "FetchCoreTask"
