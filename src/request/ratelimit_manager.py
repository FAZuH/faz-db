import asyncio
import logging
from time import time

logger = logging.getLogger("vindicator.ratelimit")


class RatelimitManager:

    def __init__(self) -> None:
        self._total: int = 300
        self._remaining: int = 300
        self.reset: float = 60.0

    @property
    def total(self) -> int:
        return self._total

    @property
    def remaining(self) -> int:
        if self.reset < 0:
            return self.total
        else:
            return self._remaining

    # @property
    # def reset(self) -> int:
    #     if self._reset == -1.0:
    #         return -1.0
    #     else:
    #         return self._reset - time()

    async def limit(self) -> None:
        if self.remaining <= 1:
            logger.info(f"You are being ratelimited, waiting for {self.reset:.2f}s")
            await asyncio.sleep(self.reset)

    def update(self, headers: dict) -> None:
        self._remaining -= 1
        # self._total = int(headers.get("ratelimit-limit", 180))
        # self._remaining = int(headers.get("ratelimit-remaining", 180))
        # self._reset = time() + int(headers.get("ratelimit-reset", 0))
