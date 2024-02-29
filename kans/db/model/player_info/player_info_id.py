from __future__ import annotations
from typing import TypedDict


class PlayerInfoId:

    def __init__(self, uuid: str) -> None:
        self._uuid = uuid

    class IdType(TypedDict):
        uuid: str

    @property
    def uuid(self) -> str:
        return self._uuid
