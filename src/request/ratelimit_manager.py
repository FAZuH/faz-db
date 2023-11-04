import asyncio
import logging
from time import time
from typing import Optional


class RatelimitManager:

    def __init__(self, total: int, sleep: int) -> None:
        self._remaining: int = total
        self.total: int = total
        self.sleep: int = sleep

    async def limit(self) -> None:
        if self.remaining <= 1:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        await asyncio.sleep(self.sleep)
        self._remaining = self.total

    def update(self, header: Optional[dict] = None) -> None:
        self._remaining -= 1

    @property
    def remaining(self) -> int:
        return self._remaining
