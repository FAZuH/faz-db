from typing import Protocol

from kans import GuildMemberHistory, GuildMemberHistoryId, TableProtocol


class GuildMemberHistoryRepo(TableProtocol[GuildMemberHistory, GuildMemberHistoryId], Protocol):
    ...
