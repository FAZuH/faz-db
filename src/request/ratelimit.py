import asyncio
from typing import Optional

from loguru import logger


class Ratelimit:

    def __init__(self, total: int, sleep: int) -> None:
        self._remaining: int = total
        self.total: int = total
        self.sleep: int = sleep

    async def limit(self) -> None:
        if self._remaining <= 1:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        logger.warning("RATELIMITED")
        await asyncio.sleep(self.sleep)
        self._remaining = self.total

    def update(self, header: Optional[dict] = None) -> None:
        self._remaining -= 1
