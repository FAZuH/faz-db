from typing import Protocol

from vindicator import GuildHistory, GuildHistoryId, Table


class GuildHistoryRepo(Table[GuildHistory, GuildHistoryId], Protocol):
    ...
