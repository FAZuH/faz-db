import asyncio
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List, Set, TypeAlias, Union
from uuid import UUID

from discord.ext.tasks import loop
from loguru import logger

from .wynncraft_request import WynncraftRequest
from constants import FETCH_ONLINE_INTERVAL, DatabaseTables
from database.vindicator_database import VindicatorDatabase
from webhook.vindicator_webhook import VindicatorWebhook

if TYPE_CHECKING:
    from objects.wynncraft_response import OnlinePlayerList

Timestamp: TypeAlias = float
Username: TypeAlias = str
Uuid: TypeAlias = UUID

lUsername: TypeAlias = List[Username]
lUuid: TypeAlias = List[Uuid]
sUsername: TypeAlias = Set[Username]
sUuid: TypeAlias = Set[Uuid]


class FetchOnline:

    _latest_req_timestamp: Timestamp
    _logoffs: sUuid = set()
    _logons: sUuid = set()
    _logon_timestamps: Dict[UUID, Timestamp] = {}
    _online_uuids: Dict[UUID, Username] = {}
    _prev_online_uuids: sUuid = set()
    _raw_online_uuids: "OnlinePlayerList"

    @staticmethod
    async def ainit():
        _wynn_req: WynncraftRequest = WynncraftRequest()  # TODO: make wynnreq methods static

    @loop(seconds=FETCH_ONLINE_INTERVAL)
    async def run() -> None:
        t0: float = perf_counter()
        logger.info(f"Running loop")

        await FetchOnline._request_api()
        asyncio.create_task(FetchOnline._update_db_player_main_info())
        FetchOnline._update_online_info()
        await FetchOnline._to_db_player_activity()

        asyncio.create_task(VindicatorWebhook.send("fetch_online", "success",
            f"**logoffs**={len(FetchOnline._logoffs)}\n"
            f"**logons**={len(FetchOnline._logons)}\n"
            f"**online**={FetchOnline._raw_online_uuids['total']}\n"
            f"**t**={perf_counter()-t0:.2f}"
        ))

    @staticmethod
    async def _request_api() -> None:
        """Assigns
        -----------
            - `FetchOnline.raw_online_player_list`
            - `FetchOnline._timestamp`
            - `FetchOnline._online_player_count`
        """
        online_uuids: Union[BaseException, "OnlinePlayerList"] = await FetchOnline._wynn_req.get_online_uuids()
        while True:
            online_uuids = await FetchOnline._wynn_req.get_online_uuids()
            if isinstance(online_uuids, dict):
                break
            await asyncio.sleep(10)

        FetchOnline._raw_online_uuids = online_uuids
        FetchOnline._latest_req_timestamp = time()

    @staticmethod
    async def _update_db_player_main_info() -> None:
        """Updates server column in player_main_info table.

        Needs
        -----------
            - `FetchOnline.raw_online_player_list`
        """
        await VindicatorDatabase.write(f"UPDATE {DatabaseTables.PLAYER_MAIN_INFO} SET server = NULL")
        asyncio.create_task(VindicatorDatabase.write_many(
            f"UPDATE {DatabaseTables.PLAYER_MAIN_INFO} SET server = %(server)s WHERE uuid = %(uuid)s",
            [{"server": server, "uuid": uuid} for uuid, server in FetchOnline._raw_online_uuids["players"].items()]))

    @staticmethod
    def _update_online_info() -> None:
        """Needs
        -----------
            - `FetchOnline._online_uuids`

        Assigns
        -----------
            - `FetchOnline._logoffs`
            - `FetchOnline._logons`

        Modifies
        -----------
            - `FetchOnline._logons_timestamp`
        """
        online_uuids: sUuid = {UUID(uuid) for uuid in FetchOnline._raw_online_uuids["players"].keys()}

        FetchOnline._logoffs = FetchOnline._prev_online_uuids - online_uuids  #
        FetchOnline._logons = online_uuids - FetchOnline._prev_online_uuids  #

        FetchOnline._prev_online_uuids = online_uuids.copy()  #

        for uuid in FetchOnline._logoffs:
            del FetchOnline._logon_timestamps[uuid]

        for uuid in FetchOnline._logons:
            FetchOnline._logon_timestamps[uuid] = FetchOnline._latest_req_timestamp

    @staticmethod
    async def _to_db_player_activity() -> None:
        """Needs
        -----------
            - `FetchOnline._logon_timestamps`
            - `FetchOnline._online_uuids`
            - `FetchOnline._timestamp`
        """
        logon_timestamps = FetchOnline._logon_timestamps.copy()
        for uuid, username in FetchOnline._online_uuids.copy().items():
            if username in logon_timestamps:
                logon_timestamps[uuid] = logon_timestamps[username]
                del logon_timestamps[username]

        params: List[dict] = [{
                "uuid": uuid.bytes,
                "logon_timestamp": logon_timestamp,
                "logoff_timestamp": FetchOnline._latest_req_timestamp
            }
            for uuid, logon_timestamp in logon_timestamps.items()
        ]
        query: str = (
            f"INSERT INTO {DatabaseTables.PLAYER_ACTIVITY} (uuid, logon_timestamp, logoff_timestamp) "
            "VALUES (%(uuid)s, %(logon_timestamp)s, %(logoff_timestamp)s) "
            "ON DUPLICATE KEY UPDATE "
            "    logoff_timestamp = VALUES(logoff_timestamp)"
        )
        asyncio.create_task(VindicatorDatabase.write_many(query, params))
