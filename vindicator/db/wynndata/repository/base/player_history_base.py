from typing import Protocol

from vindicator import PlayerHistory, PlayerHistoryId, Table


class PlayerHistoryBase(Table[PlayerHistory, PlayerHistoryId], Protocol):
    ...
