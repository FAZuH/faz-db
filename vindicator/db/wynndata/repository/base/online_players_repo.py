from typing import TYPE_CHECKING, Iterable, Protocol

from vindicator import OnlinePlayers, OnlinePlayersId, Table

if TYPE_CHECKING:
    from aiomysql import Connection


class OnlinePlayersRepo(Table[OnlinePlayers, OnlinePlayersId], Protocol):
    ...
