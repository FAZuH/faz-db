from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import PlayersResponse, Request, RequestLevel

if TYPE_CHECKING:
    from vindicator import FetchCore


class OnlineRequest(Request[PlayersResponse]):

    def __init__(self, fetch_core: FetchCore, request_arg: str = '') -> None:
        super().__init__(fetch_core, RequestLevel.ONLINE, request_arg)

    @override
    async def run(self) -> None:
        self.response = await self._fetch_core.wynnapi.get_online_uuids()
        self._done = True

    @override
    async def requeue(self) -> None:
        await asyncio.sleep(self.response.get_expiry_timediff().total_seconds())
        self._fetch_core.queue.put(
            (
                self.response.get_expiry_datetime().timestamp(),
                self.__class__(self._fetch_core, self._request_arg)
            )
        )
