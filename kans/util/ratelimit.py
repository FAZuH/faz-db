from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from loguru import Logger


class Ratelimit:

    def __init__(self, total: int, sleep: int, logger: Logger) -> None:
        self._remaining = total
        self._total = total
        self._logger = logger

        self._ratelimited = False
        self._reset: float = 0.0

    async def limit(self) -> None:
        if self._remaining <= 1:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        self._logger.warning(f"Ratelimited, waiting for {self._reset}")

        # HACK: Code below is to check if Ratelimit is already preparing to reset self._remaining
        # This is to prevent the Ratelimit from resetting self._remaining multiple times when
        # the api is being requested many times at once asynchronously. Why does this happen?
        # Because self._remaining stays below 1 until self.update() is called after an api response.

        is_first_ratelimited = False  # Is the Ratelimit already preparing to reset self._remaining?
        if not self._ratelimited:
            self._ratelimited = True
            is_first_ratelimited = True

        await asyncio.sleep(self._reset)

        if is_first_ratelimited and self._remaining <= 1:
            self._remaining = self._total
            self._ratelimited = False

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
