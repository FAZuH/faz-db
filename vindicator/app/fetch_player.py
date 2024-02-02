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
from vindicator.db.wynndata.model.character_history.character_history import CharacterHistory
from vindicator.db.wynndata.model.character_info.character_info import CharacterInfo
from vindicator.db.wynndata.model.player_history.player_history import PlayerHistory
from vindicator.db.wynndata.model.player_info.player_info import PlayerInfo

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
        reqs: list[PlayerRequest] = []
        resps: list[PlayerResponse] = []
        for req in self._request_pop_iterator():
            reqs.append(req)
            resps.append(req.response)

        # internal data processing
        online_guilds: set[str] = set()  # placeholder for new self._prev_online_guilds data
        logged_on_guilds: set[str] = set()
        for resp in resps:
            player: Player = resp.body
            if player.guild is None:
                continue

            guild_name: str = player.guild.name

            online_guilds.add(guild_name)
            if guild_name not in self._prev_online_guilds:
                logged_on_guilds.add(guild_name)

        self._prev_online_guilds = online_guilds.copy()

        # to db
        logger.debug(f"Saving to db {len(reqs)} responses")
        playerinfo: tuple[PlayerInfo, ...] = PlayerInfo.from_responses(resps)
        characterinfo: tuple[CharacterInfo, ...] = CharacterInfo.from_responses(resps)
        playerhistory: tuple[PlayerHistory, ...] = PlayerHistory.from_responses(resps)
        characterhistory: tuple[CharacterHistory, ...] = CharacterHistory.from_responses(resps)
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.wynnrepo.player_info_repository.insert(playerinfo))
            tg.create_task(self.wynnrepo.character_info_repository.insert(characterinfo))
            tg.create_task(self.wynnrepo.player_history_repository.insert(playerhistory))
            tg.create_task(self.wynnrepo.character_history_repository.insert(characterhistory))

        for req in reqs:
            # Requeue logic
            if req.response.body.online is True:
                asyncio.create_task(req.requeue())

        # queue newly logged on guilds
        for guild_name in logged_on_guilds:
            # Timestamp doesn't matter here
            self.fetch_core.queue.put((dt.now().timestamp(), GuildRequest(self.fetch_core, guild_name)))
