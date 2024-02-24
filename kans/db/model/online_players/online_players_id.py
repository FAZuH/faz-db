from .. import UuidColumn


class OnlinePlayersId:

    def __init__(self, uuid: bytes | UuidColumn) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid
