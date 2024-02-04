from __future__ import annotations
from typing import TYPE_CHECKING

from typing_extensions import override

from kans import (
    AbstractFetch,
    OnlinePlayers,
    PlayerActivityHistory,
    PlayersResponse,
)

if TYPE_CHECKING:
    from datetime import datetime as dt
    from kans import App, RequestQueue


class FetchOnlineTask(AbstractFetch[PlayersResponse]):
    """extends `AbstractFetch[PlayersResponse]`
    implements `TaskBase`"""

    def __init__(self, app: App, request_queue: RequestQueue) -> None:
        super().__init__(app, request_queue)

        self._logon_timestamps: dict[str, dt] = {}
        self._prev_online_uuids: set[str] = set()

        self.request_queue.put(0, self.app.wynnapi.get_online_uuids)

    @override
    async def _run(self) -> None:
        # get new resources
        resps = tuple(self.popall_unprocessed_response())
        if not resps:
            return

        for resp in resps:
            # internal data processing
            online_uuids: set[str] = {str(uuid) for uuid in resp.body.players}

            logged_off: set[str] = self._prev_online_uuids - online_uuids
            logged_on: set[str] = online_uuids - self._prev_online_uuids

            self._prev_online_uuids = online_uuids.copy()

            for uuid in logged_off:
                del self._logon_timestamps[uuid]

            for uuid in logged_on:
                self._logon_timestamps[uuid] = resp.get_datetime()

            # queue newly logged on players
            for uuid in logged_on:
                self.request_queue.put(
                    0,
                    self._app.wynnapi.get_player_stats,
                    uuid
                )

            # to db
            playeractivityhistory = tuple(
                PlayerActivityHistory(
                    uuid.username_or_uuid,
                    self._logon_timestamps[uuid.username_or_uuid],
                    resp.get_datetime()
                )
                for uuid in resp.body.players
                if (uuid.is_uuid() and uuid.username_or_uuid in logged_on)
            )
            self._app.logger.debug("Saving to db")
            await self._app.wynnrepo.online_players_repository.insert(OnlinePlayers.from_response(resp))
            await self._app.wynnrepo.player_activity_history_repository.insert(playeractivityhistory)

            # always requeue
            self.request_queue.put(resp.get_expiry_datetime().timestamp(), self.app.wynnapi.get_online_uuids)

    @property
    @override
    def first_delay(self) -> float:
        return 1.0

    @property
    @override
    def interval(self) -> float:
        return 15.0

    @property
    @override
    def name(self) -> str:
        return "FetchOnlineTask"
