from typing import Protocol

from vindicator import PlayerActivityHistory, PlayerActivityHistoryId, Table


class PlayerActivityHistoryRepo(Table[PlayerActivityHistory, PlayerActivityHistoryId], Protocol):
    ...
