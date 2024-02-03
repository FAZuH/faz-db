from typing import Protocol

from kans import GuildHistory, GuildHistoryId, TableProtocol


class GuildHistoryRepo(TableProtocol[GuildHistory, GuildHistoryId], Protocol):
    ...
