from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from aiomysql import Connection


class ConnectionPool(Protocol):
    """<<interface>>"""
    def get_connection(self) -> None | Connection: ...
    def release_connection(self, conn: Connection) -> None: ...
