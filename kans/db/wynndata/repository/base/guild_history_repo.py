from typing import Protocol

from src import GuildHistory, GuildHistoryId, TableProtocol


class GuildHistoryRepo(TableProtocol[GuildHistory, GuildHistoryId], Protocol):
    ...
