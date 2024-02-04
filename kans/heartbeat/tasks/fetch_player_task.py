from __future__ import annotations
from typing import TYPE_CHECKING

from typing_extensions import override

from kans import (
    logger,
    AbstractFetch,
    CharacterHistory,
    CharacterInfo,
    Player,
    PlayerHistory,
    PlayerInfo,
    PlayerResponse,
)

if TYPE_CHECKING:
    from kans import App, RequestQueue


class FetchPlayerTask(AbstractFetch[PlayerResponse]):
    """extends `AbstractFetch[PlayerResponse]`
    implements `TaskBase`"""

    def __init__(self, app: App, request_queue: RequestQueue) -> None:
        super().__init__(app, request_queue)

        self._prev_online_guilds: set[str] = set()
        """To find newly logged in guilds."""

    async def _run(self) -> None:
        resps = tuple(self.popall_unprocessed_response())
        if len(resps) == 0:
            return

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
        logger.debug(f"Saving to db {len(resps)} responses")
        await self.app.wynnrepo.player_info_repository.insert(PlayerInfo.from_responses(resps))
        await self.app.wynnrepo.character_info_repository.insert(CharacterInfo.from_responses(resps))
        await self.app.wynnrepo.player_history_repository.insert(PlayerHistory.from_responses(resps))
        await self.app.wynnrepo.character_history_repository.insert(CharacterHistory.from_responses(resps))

        for resp in resps:
            # requeue if player is online
            if resp.body.online is True:
                self.request_queue.put(
                    resp.get_expiry_datetime().timestamp(),
                    self._app.wynnapi.get_player_stats,
                    resp.body.uuid.uuid
                )

        # queue newly logged on guilds
        for guild_name in logged_on_guilds:
            # Timestamp doesn't matter here
            self.request_queue.put(0, self.app.wynnapi.get_guild_stats, guild_name)

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
        return "FetchPlayerTask"
