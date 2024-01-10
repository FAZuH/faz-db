from __future__ import annotations

from vindicator import (
    Logger,
    WynncraftDataDatabase,
)
from vindicator.constants import *
from vindicator.typehints import *


class PlayerActivityUtil:

    def __init__(self, request_sqldt: str, logon_datetime: Dict[UUID, str]) -> None:
        self._request_sqldt: str = request_sqldt
        self._logon_datetime: Dict[UUID, str] = logon_datetime

    @Logger.logging_decorator
    async def to_db(self) -> None:
        params: List[PlayerActivityDB_I] = [{
                "uuid": uuid.bytes,
                "logon_datetime": logon_dt,
                "logoff_datetime": self._request_sqldt
            }
            for uuid, logon_dt in self._logon_datetime.copy().items()
        ]
        query: str = (
            f"INSERT INTO {PLAYER_ACTIVITY} (uuid, logon_datetime, logoff_datetime) "
            "VALUES (%(uuid)s, %(logon_datetime)s, %(logoff_datetime)s) "
            "ON DUPLICATE KEY UPDATE "
            "    logoff_datetime = VALUES(logoff_datetime)"
        )
        await WynncraftDataDatabase.execute(query, params)