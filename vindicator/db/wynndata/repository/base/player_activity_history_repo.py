from typing import Protocol

from vindicator import PlayerActivityHistory, PlayerActivityHistoryId, TableProtocol


class PlayerActivityHistoryRepo(TableProtocol[PlayerActivityHistory, PlayerActivityHistoryId], Protocol):
    ...
