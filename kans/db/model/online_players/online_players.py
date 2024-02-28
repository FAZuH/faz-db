from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import OnlinePlayersId

if TYPE_CHECKING:
    from .. import UuidColumn


class OnlinePlayers(OnlinePlayersId):
    """implements `OnlinePlayersId`

    id: `uuid`"""

    def __init__(self, uuid: bytes | UuidColumn, server: str) -> None:
        super().__init__(uuid)
        self._server = server

    def to_dict(self) -> dict[str, Any]:
        return {
                "uuid": self.uuid.uuid,
                "server": self.server
        }

    @property
    def server(self) -> str:
        return self._server
