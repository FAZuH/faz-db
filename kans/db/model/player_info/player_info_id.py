from __future__ import annotations
from typing import TypedDict

from .. import UuidColumn


class PlayerInfoId:

    def __init__(self, uuid: bytes | UuidColumn) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)

    def to_dict(self) -> PlayerInfoId.Type:
        return {
                "uuid": self.uuid.uuid
        }

    class Type(TypedDict):
        uuid: bytes

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid
