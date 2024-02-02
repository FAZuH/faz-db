from typing import Protocol

from vindicator import GuildHistory, GuildHistoryId, TableProtocol


class GuildHistoryRepo(TableProtocol[GuildHistory, GuildHistoryId], Protocol):
    ...
