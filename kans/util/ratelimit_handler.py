from __future__ import annotations
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from kans import Logger


class RatelimitHandler(Protocol):
    def __init__(self, total: int, logger: Logger) -> None: ...
    async def limit(self) -> None: ...
    async def ratelimited(self) -> None: ...
    def update(self, headers: dict[str, Any]) -> None: ...
    @property
    def min_limit(self) -> int: ...
    @property
    def remaining(self) -> int: ...
    @property
    def total(self) -> int: ...
    @property
    def reset(self) -> float: ...
