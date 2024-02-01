from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from vindicator import (
    logger,
    Fetch,
    PlayerRequest,
    OnlineRequest,
)

if TYPE_CHECKING:
    from vindicator import FetchCore


class FetchOnline(Fetch[OnlineRequest]):

    def __init__(self, fetch_core: FetchCore) -> None:
        super().__init__(fetch_core)
        self.fetch_core.queue.put((0.0, OnlineRequest(fetch_core)))
        self._logon_timestamps: dict[str, float] = {}
        self._prev_online_uuids: set[str] = set()

    async def run(self) -> None:
        # Check if there's finished request. If yes, process it. Requeue after.
        if len(self._request) == 0:
            return

        # get new resources
        finished_request: OnlineRequest = self._request.pop()

        # internal data processing
        online_uuids: set[str] = {str(uuid) for uuid in finished_request.response.body.players}

        logged_off: set[str] = self._prev_online_uuids - online_uuids
        logged_on: set[str] = online_uuids - self._prev_online_uuids

        self._prev_online_uuids = online_uuids.copy()

        for uuid in logged_off:
            del self._logon_timestamps[uuid]

        for uuid in logged_on:
            self._logon_timestamps[uuid] = finished_request.response.get_datetime().timestamp()

        # queue newly logged on players
        for uuid in logged_on:
            self.fetch_core.queue.put((finished_request.response.get_datetime().timestamp(), PlayerRequest(self.fetch_core, uuid)))

        # to db
        logger.debug("Saving to db")
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.wynnrepo.online_players_repository.to_db(finished_request.response.body))
            tg.create_task(self.wynnrepo.player_activity_history_repository.to_db(finished_request.response.body, self._logon_timestamps))

        asyncio.create_task(finished_request.requeue())
