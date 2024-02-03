from typing import Protocol

from src import PlayerHistory, PlayerHistoryId, TableProtocol


class PlayerHistoryRepo(TableProtocol[PlayerHistory, PlayerHistoryId], Protocol):
    ...
