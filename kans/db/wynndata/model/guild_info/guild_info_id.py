from typing import Protocol


class GuildInfoId(Protocol):
    @property
    def name(self) -> str: ...
