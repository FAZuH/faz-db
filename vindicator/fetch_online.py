from __future__ import annotations
from asyncio import create_task, gather
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List
from uuid import UUID

from discord.ext.tasks import loop

from vindicator import (
    FETCH_ONLINE_INTERVAL,
    DatabaseTables,
    VindicatorDatabase,
    VindicatorWebhook,
    WynncraftRequest,
)

if TYPE_CHECKING:
    from asyncio import Task

    from vindicator import OnlinePlayerList, sUuid, Timestamp


class FetchOnline:

    _logged_off: sUuid = set()
    _logged_on: sUuid = set()  # used in FetchPlayer
    _logon_timestamps: Dict[UUID, Timestamp] = {}
    _online_req_timestamp: Timestamp  # used in FetchPlayer
    _online_uuids: sUuid = set()  # used in FetchPlayer
    _prev_online_uuids: sUuid = set()
    _raw_online_uuids: OnlinePlayerList

    @classmethod
    def get_logged_on(cls) -> sUuid:
        return cls._logged_on.copy()

    @classmethod
    def get_online_req_timestamp(cls) -> Timestamp:
        return cls._online_req_timestamp

    @classmethod
    def get_online_uuids(cls) -> sUuid:
        return cls._online_uuids.copy()

    @classmethod
    @loop(seconds=FETCH_ONLINE_INTERVAL)
    async def run(cls) -> None:
        t0: float = perf_counter()

        await cls._request_api()
        task1: Task = create_task(cls._update_db_player_main_info())
        cls._update_online_info()
        task2: Task = create_task(cls._to_db_player_activity())

        await gather(task1, task2)

        t1: float = perf_counter()
        create_task(VindicatorWebhook.log("fetch_online", "success", {
            "logged off": len(cls._logged_off),
            "logged on": len(cls._logged_on),
            "online": cls._raw_online_uuids["total"],
            "time spent": f"{t1-t0:.2f}s"
        }, title="FetchOnline loop finished"))

    @classmethod
    async def _request_api(cls) -> None:
        """Assigns
        -----------
            - `cls._raw_online_uuids`
            - `cls._online_uuids`
            - `cls._online_req_timestamp`
        """; t0: float = perf_counter()
        cls._raw_online_uuids = await WynncraftRequest.get_online_uuids(); t1: float = perf_counter()
        cls._online_uuids = {UUID(uuid) for uuid in cls._raw_online_uuids["players"]}
        cls._online_req_timestamp = time()

        create_task(VindicatorWebhook.log("wynncraft_request", "request", {
            "endpoint": "onlinePlayers",
            "time spent": f"{t1-t0:.2f}s"
        }, title="Get online UUIDs"))

    @classmethod
    async def _update_db_player_main_info(cls) -> None:
        """Updates server column in player_main_info table.

        Needs
        -----------
            - `cls.raw_online_player_list`
        """; t0: float = perf_counter()
        await VindicatorDatabase.write(f"UPDATE {DatabaseTables.PLAYER_MAIN_INFO} SET server = NULL")
        await VindicatorDatabase.write_many(
            f"UPDATE {DatabaseTables.PLAYER_MAIN_INFO} SET server = %(server)s WHERE uuid = %(uuid)s",
            [{"server": server, "uuid": uuid}
             for uuid, server in cls._raw_online_uuids["players"].items()]
        ); t1: float = perf_counter()

        create_task(VindicatorWebhook.log("database", "update", {
            "table": "player_main_info",
            "records": len(cls._raw_online_uuids["players"]),
            "time spent": f"{t1-t0:.2f}s"
        }, title="Update players' servers"))

    @classmethod
    def _update_online_info(cls) -> None:
        """Needs
        -----------
            - `cls._online_uuids`

        Assigns
        -----------
            - `cls._logoffs`
            - `cls._logons`

        Modifies
        -----------
            - `cls._logons_timestamp`
        """
        online_uuids: sUuid = cls._online_uuids.copy()

        # TODO: use timestamps, to make sure queue update in FetchPlayer is consistent
        cls._logged_off = cls._prev_online_uuids - online_uuids  #
        cls._logged_on = online_uuids - cls._prev_online_uuids  #

        cls._prev_online_uuids = online_uuids.copy()  #

        for uuid in cls._logged_off:
            del cls._logon_timestamps[uuid]

        for uuid in cls._logged_on:
            cls._logon_timestamps[uuid] = cls._online_req_timestamp

    @classmethod
    async def _to_db_player_activity(cls) -> None:
        """Needs
        -----------
            - `cls._logon_timestamps`
            - `cls._online_uuids`
            - `cls._timestamp`
        """
        params: List[dict] = [{
                "uuid": uuid.bytes,
                "logon_timestamp": logon_timestamp,
                "logoff_timestamp": cls._online_req_timestamp
            }
            for uuid, logon_timestamp in cls._logon_timestamps.copy().items()
        ]
        query: str = (
            f"INSERT INTO {DatabaseTables.PLAYER_ACTIVITY} (uuid, logon_timestamp, logoff_timestamp) "
            "VALUES (%(uuid)s, %(logon_timestamp)s, %(logoff_timestamp)s) "
            "ON DUPLICATE KEY UPDATE "
            "    logoff_timestamp = VALUES(logoff_timestamp)"
        )
        t0: float = perf_counter()
        await VindicatorDatabase.write_many(query, params); t1: float = perf_counter()

        create_task(VindicatorWebhook.log("database", "write", {
            "table": "player_activity",
            "records": len(params),
            "time spent": f"{t1-t0:.2f}s"
        }, title="Write player activities"))
