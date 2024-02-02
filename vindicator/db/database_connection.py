from __future__ import annotations
from typing import TYPE_CHECKING

from .connection_pool import ConnectionPool

if TYPE_CHECKING:
    from aiomysql import Connection


class DatabaseConnection(ConnectionPool):
    """<<interface>>"""
    def get_connection(self) -> None | Connection: ...
    def release_connection(self, conn: Connection) -> None: ...