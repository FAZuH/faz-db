from __future__ import annotations
import asyncio
from datetime import datetime as dt
from typing import TYPE_CHECKING

from vindicator import (
    logger,
    Fetch,
    GuildRequest,
    Player,
    PlayerRequest,
    PlayerResponse,
)

if TYPE_CHECKING:
    from vindicator import FetchCore


class FetchPlayer(Fetch[PlayerRequest]):

    def __init__(self, fetch_core: FetchCore) -> None:
        super().__init__(fetch_core)
        self._prev_online_guilds: set[str] = set()
        """To find newly logged in guilds."""

    async def run(self) -> None:
        # Check if there's finished request. If yes, process it. Requeue after.
        if len(self._request) == 0:
            return

        # get new resources
        finished_requests: list[PlayerRequest] = []
        responses: list[PlayerResponse] = []
        for req in self._request_pop_iterator():
            finished_requests.append(req)
            responses.append(req.response)

        # internal data processing
        online_guilds: set[str] = set()  # placeholder for new self._prev_online_guilds data
        logged_on_guilds: set[str] = set()
        for resp in responses:
            player: Player = resp.body
            if player.guild is None:
                continue

            guild_name: str = player.guild.name

            online_guilds.add(guild_name)
            if guild_name not in self._prev_online_guilds:
                logged_on_guilds.add(guild_name)

        self._prev_online_guilds = online_guilds.copy()

        # to db
        logger.debug(f"Saving to db {len(finished_requests)} responses")
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.wynnrepo.player_info_repository.to_db(responses))
            tg.create_task(self.wynnrepo.character_info_repository.to_db(responses))
            tg.create_task(self.wynnrepo.player_history_repository.to_db(responses))
            tg.create_task(self.wynnrepo.character_history_repository.to_db(responses))

        for req in finished_requests:
            # Requeue logic
            if req.response.body.online is True:
                asyncio.create_task(req.requeue())

        # queue newly logged on guilds
        for guild_name in logged_on_guilds:
            # Timestamp doesn't matter here
            self.fetch_core.queue.put((dt.now().timestamp(), GuildRequest(self.fetch_core, guild_name)))
