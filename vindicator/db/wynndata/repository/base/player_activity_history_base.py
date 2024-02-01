from typing import Protocol

from vindicator import PlayerActivityHistory, PlayerActivityHistoryId, Table


class PlayerActivityHistoryBase(Table[PlayerActivityHistory, PlayerActivityHistoryId], Protocol):
    ...
