from typing import Protocol

from vindicator import OnlinePlayers, OnlinePlayersId, Table


class OnlinePlayersBase(Table[OnlinePlayers, OnlinePlayersId], Protocol):
    ...
