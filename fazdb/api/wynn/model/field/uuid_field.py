from uuid import UUID


class UuidField:

    def __init__(self, uuid_: str) -> None:
        self._uuid: str = uuid_

    def to_bytes(self) -> bytes:
        return UUID(self._uuid).bytes

    @property
    def uuid(self) -> str:
        return self._uuid
