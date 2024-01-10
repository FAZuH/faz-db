from __future__ import annotations
from uuid import UUID

from vindicator import (
    Logger,
    WynncraftDataDatabase,
)
from vindicator.constants import *
from vindicator.typehints import *


class PlayerServerUtil:

    def __init__(self, raw_online_uuids: OnlinePlayerList) -> None:
        self._raw_online_uuids: OnlinePlayerList = raw_online_uuids

    @Logger.logging_decorator
    async def to_db(self) -> None:
        async with WynncraftDataDatabase.transaction_group() as tg:
            tg.add(f"DELETE FROM {PLAYER_SERVER} WHERE server IS NOT NULL")
            tg.add(
                f"INSERT INTO {PLAYER_SERVER} (uuid, server) VALUES (%(uuid)s, %(server)s)",
                [{"server": server, "uuid": UUID(uuid).bytes} for uuid, server in self._raw_online_uuids["players"].items()]
            )
