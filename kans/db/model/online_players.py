from __future__ import annotations

from kans import UuidColumn


class OnlinePlayers:
    """implements `OnlinePlayersId`

    id: `uuid`"""

    def __init__(self, uuid: bytes | UuidColumn, server: str) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._server = server

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def server(self) -> str:
        return self._server
