from typing import Protocol

from src import PlayerActivityHistory, PlayerActivityHistoryId, TableProtocol


class PlayerActivityHistoryRepo(TableProtocol[PlayerActivityHistory, PlayerActivityHistoryId], Protocol):
    ...
