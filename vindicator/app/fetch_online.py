from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from vindicator import (
    logger,
    AbstractFetch,
    PlayerActivityHistory,
    PlayerRequest,
    OnlineRequest,
    OnlinePlayers
)

if TYPE_CHECKING:
    from datetime import datetime as dt
    from vindicator import FetchCore


class FetchOnline(AbstractFetch[OnlineRequest]):
    """extends `Fetch`"""

    def __init__(self, fetch_core: FetchCore) -> None:
        super().__init__(fetch_core)
        self.fetch_core.queue.put(OnlineRequest(fetch_core, 0))
        self._logon_timestamps: dict[str, dt] = {}
        self._prev_online_uuids: set[str] = set()

    async def run(self) -> None:
        # Check if there's finished request. If yes, process and requeue.
        if len(self._request) == 0:
            return

        # get new resources
        req: OnlineRequest = self._request.pop()

        # internal data processing
        online_uuids: set[str] = {str(uuid) for uuid in req.response.body.players}

        logged_off: set[str] = self._prev_online_uuids - online_uuids
        logged_on: set[str] = online_uuids - self._prev_online_uuids

        self._prev_online_uuids = online_uuids.copy()

        for uuid in logged_off:
            del self._logon_timestamps[uuid]

        for uuid in logged_on:
            self._logon_timestamps[uuid] = req.response.get_datetime()

        # queue newly logged on players
        for uuid in logged_on:
            self.fetch_core.queue.put(PlayerRequest(
                self.fetch_core, req.response.get_datetime().timestamp(), uuid
            ))

        # to db
        onlineplayers: tuple[OnlinePlayers, ...] = OnlinePlayers.from_response(req.response)
        playeractivityhistory = tuple(
            PlayerActivityHistory(
                uuid.username_or_uuid,
                self._logon_timestamps[uuid.username_or_uuid],
                req.response.get_datetime()
            )
            for uuid in req.response.body.players
            if (uuid.is_uuid() and uuid.username_or_uuid in logged_on)
        )
        logger.debug("Saving to db")
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.wynnrepo.online_players_repository.insert(onlineplayers))
            tg.create_task(self.wynnrepo.player_activity_history_repository.insert(playeractivityhistory))

        asyncio.create_task(req.requeue())
