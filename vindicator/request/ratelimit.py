import asyncio
from time import time

from loguru import logger


class Ratelimit:

    def __init__(self, total: int, sleep: int) -> None:
        self._remaining: int = total
        self._total: int = total
        self._reset: float = 0.0

    async def limit(self) -> None:
        if self._remaining <= 1:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        logger.warning(f"You are being ratelimited, waiting for {self._reset}s")
        await asyncio.sleep(self._reset)

    def update(self, headers: dict) -> None:
        self._total = int(headers.get("RateLimit-Limit", 180))
        self._remaining = int(headers.get("RateLimit-Remaining", 180))
        self._reset = int(headers.get("RateLimit-Reset", 60))
