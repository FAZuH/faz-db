from __future__ import annotations
from typing import TYPE_CHECKING

from typing_extensions import override

from kans import (
    AbstractFetch,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    GuildResponse,
)

if TYPE_CHECKING:
    from kans import App, RequestQueue


class FetchGuildTask(AbstractFetch[GuildResponse]):
    """extends `AbstractFetch[GuildResponse]`
    implements `TaskBase`"""

    def __init__(self, app: App, request_queue: RequestQueue) -> None:
        super().__init__(app, request_queue)

    @override
    async def _run(self) -> None:
        resps = tuple(self.popall_unprocessed_response())
        if len(resps) == 0:
            return

        # to db
        self.app.logger.debug(f"Saving to db {len(resps)} responses")
        await self.app.wynnrepo.guild_info_repository.insert(GuildInfo.from_responses(resps))
        await self.app.wynnrepo.guild_history_repository.insert(GuildHistory.from_responses(resps))
        await self.app.wynnrepo.guild_member_history_repository.insert(GuildMemberHistory.from_responses(resps))

        # requeue if there's online members in guild
        for resp in resps:
            if resp.body.members.get_online_members() > 0:
                self.request_queue.put(
                    resp.get_expiry_datetime().timestamp(),
                    self._app.wynnapi.get_guild_stats,
                    resp.body.name
                )

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
        return "FetchGuildTask"
