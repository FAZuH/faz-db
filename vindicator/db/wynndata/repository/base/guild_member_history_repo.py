from typing import Protocol

from vindicator import GuildMemberHistory, GuildMemberHistoryId, TableProtocol


class GuildMemberHistoryRepo(TableProtocol[GuildMemberHistory, GuildMemberHistoryId], Protocol):
    ...
