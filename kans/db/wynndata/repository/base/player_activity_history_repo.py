from typing import Protocol

from kans import PlayerActivityHistory, PlayerActivityHistoryId, TableProtocol


class PlayerActivityHistoryRepo(TableProtocol[PlayerActivityHistory, PlayerActivityHistoryId], Protocol):
    ...
