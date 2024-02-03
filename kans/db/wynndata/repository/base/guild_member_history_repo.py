from typing import Protocol

from src import GuildMemberHistory, GuildMemberHistoryId, TableProtocol


class GuildMemberHistoryRepo(TableProtocol[GuildMemberHistory, GuildMemberHistoryId], Protocol):
    ...
