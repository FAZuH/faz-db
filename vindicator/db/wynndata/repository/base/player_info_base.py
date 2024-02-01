from typing import Protocol

from vindicator import PlayerInfo, PlayerInfoId, Table



class PlayerInfoBase(Table[PlayerInfo, PlayerInfoId], Protocol):
    """<<interface>>

    implements Table[PlayerInfo, PlayerInfoId]"""
    ...
