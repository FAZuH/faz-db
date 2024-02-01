from typing import Protocol

from vindicator import GuildMemberHistory, GuildMemberHistoryId, Table


class GuildMemberHistoryRepo(Table[GuildMemberHistory, GuildMemberHistoryId], Protocol):
    ...
