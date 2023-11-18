import asyncio
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List, Set, TypeAlias, Union
from uuid import UUID

from discord.ext.tasks import loop
from loguru import logger
from mojang import API, TooManyRequests

from constants import FETCH_ONLINE_INTERVAL, DatabaseTables
from database.vindicator_database import VindicatorDatabase
from request.mojang_request import MojangRequest
from request.wynncraft_request import WynncraftRequest
from webhook.vindicator_webhook import VindicatorWebhook

if TYPE_CHECKING:
    from objects.wynncraft_response import OnlinePlayerList

Timestamp: TypeAlias = float
Username: TypeAlias = str
Uuid: TypeAlias = UUID

lUsernames: TypeAlias = List[Username]
lUuids: TypeAlias = List[Uuid]
sUsernames: TypeAlias = Set[Username]
sUuids: TypeAlias = Set[Uuid]


class FetchOnline:

    raw_online_player_list: "OnlinePlayerList"
    ts: Timestamp
    logons: sUuids = set()
    usernames_nowhere: lUsernames = []

    def __init__(self) -> None:
        self._logoffs: sUuids = set()
        self._logon_t: Dict[UUID, Timestamp] = {}
        self._online_uuids: Dict[UUID, Username] = {}
        self._prev_online_uuids: sUuids = set()

        self.mojang_req: MojangRequest = MojangRequest()
        self.wynn_req: WynncraftRequest = WynncraftRequest()
        return

    # @loop(seconds=FETCH_ONLINE_INTERVAL)
    # async def loop_run(self) -> None:
    #     asyncio.create_task(self.run())
    #     return

    @loop(seconds=FETCH_ONLINE_INTERVAL)
    async def run(self) -> None:
        t0: float = perf_counter()
        logger.info(f"Running loop")

        await self._request_api()
        await self._update_db_player_main_info()
        await self._username_to_uuid()
        self._update_online_info()
        await self._to_db_player_activity()

        await VindicatorWebhook.send("fetch_online", "success",
            f"**logoffs**={len(self._logoffs)}\n"
            f"**logons**={len(FetchOnline.logons)}\n"
            f"**online**={FetchOnline.raw_online_player_list['total']}\n"
            f"**t**={perf_counter()-t0:.2f}"
        )
        return

    async def _request_api(self) -> None:
        """Assigns
        -----------
            - `FetchOnline.raw_online_player_list`
            - `FetchOnline._timestamp`
            - `self._online_player_count`
        """
        online_players: Union[BaseException, "OnlinePlayerList"] = await self.wynn_req.get_online_player_json()
        while not isinstance(online_players, dict):
            online_players = await self.wynn_req.get_online_player_json()
        FetchOnline.raw_online_player_list = online_players
        FetchOnline._timestamp = time()
        return

    async def _update_db_player_main_info(self) -> None:
        """Updates server column in player_main_info table.

        Needs
        -----------
            - `FetchOnline.raw_online_player_list`
        """
        await VindicatorDatabase.write(f"UPDATE {DatabaseTables.PLAYER_MAIN_INFO} SET server = NULL")
        asyncio.create_task(VindicatorDatabase.write_many(
            f"UPDATE {DatabaseTables.PLAYER_MAIN_INFO} SET server = %(server)s WHERE latest_username = %(username)s",
            [{"server": server, "username": username} for username, server in FetchOnline.raw_online_player_list["players"].items()]))
        return

    async def _username_to_uuid(self) -> None:
        """Gets uuids of online players.

        Needs
        -----------
            - `FetchOnline.raw_online_player_list`

        Assigns
        -----------
            - `self._usernames_not_in_anywhere`
            - `self._online_uuids`
        """
        usernames: sUsernames = set(FetchOnline.raw_online_player_list["players"].keys())

        params: List[dict] = [{"latest_username": username} for username in usernames]
        query: str = (
            f"SELECT latest_username, uuid FROM {DatabaseTables.PLAYER_MAIN_INFO} "
            "WHERE latest_username = %(latest_username)s"
        )
        result: List[dict] = await VindicatorDatabase.read_many(query, params)
        asyncio.create_task(VindicatorWebhook.send("fetch_online", "info", f"usernames_in_db={len(result)}"))

        online_uuids: Dict[UUID, Username] = {UUID(bytes=d["uuid"]): d["latest_username"] for d in result}
        usernames_not_in_db: lUsernames = list(usernames - set(online_uuids.values()))
        temp: sUsernames = set(usernames_not_in_db)

        n: int = 10  # Requests `n` UUIDs at a time
        if usernames_not_in_db:
            asyncio.create_task(VindicatorWebhook.send("fetch_online", "info",
                f"**usernames_not_in_db**={len(usernames_not_in_db)}. Fetching from mojang api..."
            ))
        while usernames_not_in_db:
            try:
                uuids: Dict[str, str] = await self.mojang_req.get_uuids(usernames_not_in_db[:n])
            except TooManyRequests:
                logger.warning("mojang.TooManyRequests. sleeping...")
                await asyncio.sleep(60.0)
                continue

            temp = temp - set(uuids.keys())
            online_uuids.update({UUID(uuid): username for username, uuid in uuids.items()})
            usernames_not_in_db = usernames_not_in_db[n:]

        # TODO: report to webhook
        FetchOnline.usernames_nowhere.extend(temp)
        self._online_uuids = online_uuids.copy()  #
        asyncio.create_task(VindicatorWebhook.send("fetch_online", "info",
            f"**usernames_nowhere**={len(FetchOnline.usernames_nowhere)}"
        ))
        return

    def _update_online_info(self) -> None:
        """Needs
        -----------
            - `self._online_uuids`

        Assigns
        -----------
            - `self._logoffs`
            - `FetchOnline._logons`

        Modifies
        -----------
            - `FetchOnline._logons_timestamp`
        """
        online_uuids: sUuids = set(self._online_uuids.keys())

        self._logoffs = self._prev_online_uuids - online_uuids  #
        FetchOnline.logons = online_uuids - self._prev_online_uuids  #

        self._prev_online_uuids = online_uuids.copy()  #

        for uuid in self._logoffs:
            del self._logon_t[uuid]

        for uuid in FetchOnline.logons:
            self._logon_t[uuid] = FetchOnline._timestamp
        return

    async def _to_db_player_activity(self) -> None:
        """Needs
        -----------
            - `self._logon_timestamps`
            - `self._online_uuids`
            - `FetchOnline._timestamp`
        """
        logon_timestamps = self._logon_t.copy()
        for uuid, username in self._online_uuids.copy().items():
            if username in logon_timestamps:
                logon_timestamps[uuid] = logon_timestamps[username]
                del logon_timestamps[username]

        params: List[dict] = [
            {"uuid": uuid.bytes, "logon_timestamp": logon_timestamp, "logoff_timestamp": FetchOnline._timestamp} for uuid, logon_timestamp in logon_timestamps.items()
        ]
        query: str = (
            f"INSERT INTO {DatabaseTables.PLAYER_ACTIVITY} (uuid, logon_timestamp, logoff_timestamp) "
            "VALUES (%(uuid)s, %(logon_timestamp)s, %(logoff_timestamp)s) "
            "ON DUPLICATE KEY UPDATE "
            "    logoff_timestamp = VALUES(logoff_timestamp)"
        )
        asyncio.create_task(VindicatorDatabase.write_many(query, params))
        return
