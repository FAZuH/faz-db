from __future__ import annotations
from typing import TypedDict


class OnlinePlayersId:

    def __init__(self, uuid: str | str) -> None:
        self._uuid = uuid

    class IdType(TypedDict):
        uuid: str

    @property
    def uuid(self) -> str:
        return self._uuid
