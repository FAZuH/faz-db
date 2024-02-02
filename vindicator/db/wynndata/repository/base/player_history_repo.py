from typing import Protocol

from vindicator import PlayerHistory, PlayerHistoryId, TableProtocol


class PlayerHistoryRepo(TableProtocol[PlayerHistory, PlayerHistoryId], Protocol):
    ...
