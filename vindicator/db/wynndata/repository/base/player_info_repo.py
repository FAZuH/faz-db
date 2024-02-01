from typing import Protocol

from vindicator import PlayerInfo, PlayerInfoId, Table


class PlayerInfoRepo(Table[PlayerInfo, PlayerInfoId], Protocol):
    """<<interface>>

    implements Table[PlayerInfo, PlayerInfoId]"""
    ...
