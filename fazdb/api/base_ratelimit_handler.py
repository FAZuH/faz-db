from abc import ABC, abstractmethod
import asyncio
from typing import Any

from loguru import logger


class BaseRatelimitHandler(ABC):

    async def limit(self) -> None:
        if self.remaining <= self.min_limit:
            await self.ratelimited()

    async def ratelimited(self) -> None:
        logger.warning(f"Ratelimited. Waiting for {self.reset}s")
        await asyncio.sleep(self.reset)

    @abstractmethod
    def update(self, headers: dict[str, Any]) -> None: ...
    @property
    @abstractmethod
    def min_limit(self) -> int: ...
    @property
    @abstractmethod
    def remaining(self) -> int: ...
    @property
    @abstractmethod
    def total(self) -> int: ...
    @property
    @abstractmethod
    def reset(self) -> float: ...
