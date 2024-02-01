from typing import Protocol

from vindicator import PlayerHistory, PlayerHistoryId, Table


class PlayerHistoryRepo(Table[PlayerHistory, PlayerHistoryId], Protocol):
    ...
