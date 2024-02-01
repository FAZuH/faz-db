from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from vindicator import logger, Fetch, GuildRequest

if TYPE_CHECKING:
    from vindicator import FetchCore, GuildResponse


class FetchGuild(Fetch[GuildRequest]):

    def __init__(self, fetch_core: FetchCore) -> None:
        super().__init__(fetch_core)

    async def run(self) -> None:
        # Check if there's finished request. If yes, process it. Requeue after.
        if len(self._request) == 0:
            return

        # get new resources
        finished_requests: list[GuildRequest] = []
        responses: list[GuildResponse] = []
        for req in self._request_pop_iterator():
            finished_requests.append(req)
            responses.append(req.response)

        # to db
        logger.debug(f"Saving to db {len(finished_requests)} responses")
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.wynnrepo.guild_info_repository.to_db(responses))
            tg.create_task(self.wynnrepo.guild_history_repository.to_db(responses))
            tg.create_task(self.wynnrepo.guild_member_history_repository.to_db(responses))

        for req in finished_requests:
            # Check if any members has 'online' as true
            asyncio.create_task(req.requeue())
