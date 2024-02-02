from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import PlayersResponse, AbstractRequest, RequestLevel

if TYPE_CHECKING:
    from vindicator import FetchCore


class OnlineRequest(AbstractRequest[PlayersResponse]):
    """extends `AbstractRequest`"""

    def __init__(self, fetch_core: FetchCore, weight: float) -> None:
        super().__init__(fetch_core, RequestLevel.ONLINE, weight)

    @override
    async def run(self) -> None:
        self.response = await self._fetch_core.wynnapi.get_online_uuids()
        self._done = True

    @override
    async def requeue(self) -> None:
        await asyncio.sleep(self.response.get_expiry_timediff().total_seconds())
        self._fetch_core.queue.put(self.__class__(
            self._fetch_core,
            self.response.get_expiry_datetime().timestamp(),
        ))
