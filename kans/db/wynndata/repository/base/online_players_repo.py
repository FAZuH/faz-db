from typing import Protocol

from src import OnlinePlayers, OnlinePlayersId, TableProtocol


class OnlinePlayersRepo(TableProtocol[OnlinePlayers, OnlinePlayersId], Protocol):
    ...
