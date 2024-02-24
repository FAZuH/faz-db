from __future__ import annotations
from typing import TYPE_CHECKING


from kans import UuidColumn

if TYPE_CHECKING:
    from kans import PlayersResponse


class OnlinePlayers:
    """implements `OnlinePlayersId`

    id: `uuid`"""

    def __init__(self, uuid: UuidColumn, server: str) -> None:
        self._uuid = uuid
        self._server = server

    @classmethod
    def from_response(cls, response: PlayersResponse) -> tuple[OnlinePlayers, ...]:
        return tuple(cls(
            uuid=UuidColumn(uuid.to_bytes()),
            server=server
        ) for uuid, server in response.body.iter_players())

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def server(self) -> str:
        return self._server
