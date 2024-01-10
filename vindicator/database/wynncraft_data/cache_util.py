from __future__ import annotations
from asyncio import create_task
from time import time

from vindicator import (
    WynncraftDataDatabase,
    VindicatorWebhook,
    WynncraftResponseUtil
)
from vindicator.constants import *
from vindicator.typehints import *


class CacheUtil:

    @staticmethod
    async def to_db() -> None:
        pass
