from typing import Protocol

from vindicator import GuildHistory, GuildHistoryId, Table


class GuildHistoryBase(Table[GuildHistory, GuildHistoryId], Protocol):
    ...
