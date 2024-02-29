from __future__ import annotations
from typing import TypedDict

from . import OnlinePlayersId


class OnlinePlayers(OnlinePlayersId):
    """implements `OnlinePlayersId`

    id: `uuid`"""

    def __init__(self, uuid: str | str, server: str) -> None:
        super().__init__(uuid)
        self._server = server

    class Type(TypedDict):
        uuid: str
        server: str

    @property
    def server(self) -> str:
        return self._server
