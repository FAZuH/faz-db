from __future__ import annotations
from typing import TypedDict


class GuildInfoId:

    def __init__(self, name: str) -> None:
        self._name = name

    class IdType(TypedDict):
        name: str

    @property
    def name(self) -> str:
        return self._name
