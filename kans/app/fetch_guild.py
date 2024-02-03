from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from kans import (
    logger,
    AbstractFetch,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    GuildRequest
)

if TYPE_CHECKING:
    from kans import FetchCore, GuildResponse


class FetchGuild(AbstractFetch[GuildRequest]):
    """extends `Fetch`"""

    def __init__(self, fetch_core: FetchCore) -> None:
        super().__init__(fetch_core)

    async def run(self) -> None:
        # Check if there's finished request. If yes, process it. Requeue after.
        if len(self._request) == 0:
            return

        # get new resources
        reqs: list[GuildRequest] = []
        resps: list[GuildResponse] = []
        for req in self._request_pop_iterator():
            reqs.append(req)
            resps.append(req.response)

        # to db
        guildinfo: tuple[GuildInfo, ...] = GuildInfo.from_responses(resps)
        guildhistory: tuple[GuildHistory, ...] = GuildHistory.from_responses(resps)
        guildmemberhistory = GuildMemberHistory.from_responses(resps)
        logger.debug(f"Saving to db {len(reqs)} responses")
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.wynnrepo.guild_info_repository.insert(guildinfo))
            tg.create_task(self.wynnrepo.guild_history_repository.insert(guildhistory))
            tg.create_task(self.wynnrepo.guild_member_history_repository.insert(guildmemberhistory))

        for req in reqs:
            # Check if any members has 'online' as true
            if req.response.body.members.get_online_members() > 0:
                asyncio.create_task(req.requeue())
