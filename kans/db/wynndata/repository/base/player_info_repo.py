from typing import Protocol

from kans import PlayerInfo, PlayerInfoId, TableProtocol


class PlayerInfoRepo(TableProtocol[PlayerInfo, PlayerInfoId], Protocol):
    """<<interface>>

    implements Table[PlayerInfo, PlayerInfoId]"""
    ...
