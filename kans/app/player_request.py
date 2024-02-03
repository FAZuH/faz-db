from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING
from typing_extensions import override

from src import PlayerResponse, AbstractRequest, RequestLevel

if TYPE_CHECKING:
    from src import FetchCore


class PlayerRequest(AbstractRequest[PlayerResponse]):
    """extends `AbstractRequest`"""

    def __init__(self, fetch_core: FetchCore, weight: float, request_arg: str) -> None:
        super().__init__(fetch_core, RequestLevel.PLAYER, weight, request_arg)

    @override
    async def run(self) -> None:
        self.response = await self._fetch_core.wynnapi.get_player_stats(self._request_arg)
        self._done = True

    @override
    async def requeue(self) -> None:
        await asyncio.sleep(self.response.get_expiry_timediff().total_seconds())
        self._fetch_core.queue.put(self.__class__(
            self._fetch_core,
            self.response.get_expiry_datetime().timestamp() + 480.0,
            self._request_arg
        ))
