import asyncio
import logging
from time import time

# logger = logging.getLogger("vindicator.ratelimit")


# class RatelimitManager:

#     def __init__(self, total: int) -> None:
#         self._remaining: int = total
#         self._total: int = total
#         self._reset: float = -1.0

#     @property
#     def total(self) -> int:
#         return self._total

#     @property
#     def remaining(self) -> int:
#         if self.reset < 0:
#             return self.total
#         else:
#             return self._remaining

#     @property
#     def reset(self) -> float:
#         if self._reset == -1.0:
#             return 60.0  # DEFAULT
#         else:
#             return self._reset - time()

#     async def limit(self) -> None:
#         if self.remaining <= 1:
#             # logger.info(f"You are being ratelimited, waiting for {self.reset:.2f}s")
#             await asyncio.sleep(self.reset)

#     def update(self, headers: dict) -> None:
#         self._remaining -= 1
#         # self._total = int(headers.get("ratelimit-limit", 180))
#         # self._remaining = int(headers.get("ratelimit-remaining", 180))
#         # self._reset = time() + int(headers.get("ratelimit-reset", 0))


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

    def update(self, header: dict) -> None:
        self._remaining -= 1

    @property
    def remaining(self) -> int:
        return self._remaining
