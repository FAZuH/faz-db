from typing import TYPE_CHECKING, Iterable, Protocol

from vindicator import OnlinePlayers, OnlinePlayersId, TableProtocol

if TYPE_CHECKING:
    from aiomysql import Connection


class OnlinePlayersRepo(TableProtocol[OnlinePlayers, OnlinePlayersId], Protocol):
    ...
