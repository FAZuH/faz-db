from __future__ import annotations
import asyncio
from typing import Any

from loguru import logger

from .. import RatelimitHandler
from .model.headers import Headers


class WynnRatelimitHandler(RatelimitHandler):

    def __init__(self, min_limit: int, total: int) -> None:
        self._min_limit = min_limit
        self._remaining = total
        self._total = total

        self._reset: float = 0.0

    async def limit(self) -> None:
        if self._remaining <= self.min_limit:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        logger.warning(f"Ratelimited. Waiting for {self.reset}s")
        await asyncio.sleep(self.reset)

    def update(self, headers: dict[str, Any]) -> None:
        header = Headers(headers)
        self._total = header.ratelimit_limit
        self._remaining = header.ratelimit_remaining
        self._reset = header.ratelimit_reset

    @property
    def min_limit(self) -> int:
        return self._min_limit

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def total(self) -> int:
        return self._total

    @property
    def reset(self) -> float:
        return self._reset
