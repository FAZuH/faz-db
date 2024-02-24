from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from loguru import Logger


class Ratelimit:

    def __init__(self, total: int, sleep: int, logger: Logger) -> None:
        self._remaining = total
        self._total = total
        self._reset: float = 0.0
        self._logger = logger

    async def limit(self) -> None:
        if self._remaining <= 1:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        self._logger.warning(f"Ratelimited, waiting for {self._reset}")
        await asyncio.sleep(self._reset)

    def update(self, headers: dict[str, Any]) -> None:
        self._total = int(headers.get("RateLimit-Limit", 180))
        self._remaining = int(headers.get("RateLimit-Remaining", 180))
        self._reset = int(headers.get("RateLimit-Reset", 60))

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def total(self) -> int:
        return self._total

    @property
    def reset(self) -> float:
        return self._reset
