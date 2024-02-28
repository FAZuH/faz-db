from __future__ import annotations
from typing import TypedDict


class GuildInfoId:

    def __init__(self, name: str) -> None:
        self._name = name

    def to_dict(self) -> GuildInfoId.Type:
        return {
                "name": self.name
        }

    class Type(TypedDict):
        name: str

    @property
    def name(self) -> str:
        return self._name
