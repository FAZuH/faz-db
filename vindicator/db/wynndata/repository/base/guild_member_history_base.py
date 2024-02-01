from typing import Protocol

from vindicator import GuildMemberHistory, GuildMemberHistoryId, Table


class GuildMemberHistoryBase(Table[GuildMemberHistory, GuildMemberHistoryId], Protocol):
    ...
