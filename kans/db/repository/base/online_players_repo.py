from typing import Protocol

from kans import OnlinePlayers, OnlinePlayersId, TableProtocol


class OnlinePlayersRepo(TableProtocol[OnlinePlayers, OnlinePlayersId], Protocol):
    ...
