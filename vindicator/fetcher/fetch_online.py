from __future__ import annotations
from asyncio import create_task, gather
from collections import deque
from uuid import UUID

from discord.ext.tasks import loop

from vindicator import (
    Fetch,
    Logger,
    PlayerActivityUtil,
    PlayerServerUtil,
    WynncraftRequest,
    WynncraftResponseUtil
)
from vindicator.constants import *
from vindicator.typehints import *


class FetchOnline(Fetch):

    # _logged_off: sUuid = set()
    # _logged_on: sUuid = set()  # used in FetchPlayer
    # _logon_dt: Dict[UUID, str] = {}
    # _request_timestamp: Timestamp
    # _online_uuids: sUuid = set()  # used in FetchPlayer
    # _prev_online_uuids: sUuid = set()
    # _raw_online_uuids: OnlinePlayerList

    def __init__(self, wynncraft_request: WynncraftRequest) -> None:
        self._wynncraft_request: WynncraftRequest = wynncraft_request

        self._request_queue: Dict[float, Coro[None]] = {}
        self._responses: List[ResponseSet[OnlinePlayerList, Headers]] = []
        return

    def get_request_queue(self) -> Dict[float, Coro[None]]:
        return

    def dequeue_dbquery(self) -> Dict[float, Coro[None]]:
        return

    def run(self) -> None:
        self._queue_request()
        self._queue_dbquery()
        return

    # private methods
    async def _request_coro(self, arg: str = "") -> None:
        self._responses.append(await self._wynncraft_request.get_online_uuids())
        return

    async def _dbquery_coro(self, arg: str = "") -> None:
        return

    def _queue_request(self) -> None:
        # first-time fetch
        if not self._responses:
            self._request_queue.append(self._request_coro())
        # TODO: refetch
        return

    def _queue_dbquery(self) -> None:
        coro: Coro[None] = self._dbquery_coro("foo")
        return











    @Logger.logging_decorator
    async def _run(self) -> None:
        await self._request_api()
        task1: Task[Coro[None]] = create_task(PlayerServerUtil(self._raw_online_uuids).to_db())
        self._update_online_info()
        task2: Task[Coro[None]] = create_task(PlayerActivityUtil(self._request_sqldt, self._logon_dt).to_db())
        await gather(task1, task2)

    @Logger.logging_decorator
    async def _request_api(self) -> None:
        """ Assigns
        -----------
            - `_raw_online_uuids`
            - `_online_uuids`
            - `_request_sqldt`
            - `_request_timestamp`
        """
        async with WynncraftRequest() as client:
            res = await client.get_online_uuids()
            self._raw_online_uuids = res.json
            self._online_uuids = {UUID(uuid) for uuid in res.json["players"]}
            self._request_sqldt: str = WynncraftResponseUtil.resp_to_sqldt(res.headers.get("Date", ""))
            self._request_timestamp = WynncraftResponseUtil.resp_to_timestamp(res.headers.get("Date", ""))

    def _update_online_info(self) -> None:
        """Needs
        -----------
            - `_online_uuids`

        Assigns
        -----------
            - `_logged_off`
            - `_logged_on`

        Modifies
        -----------
            - `_logon_datetime`
        """
        online_uuids: sUuid = self._online_uuids.copy()

        # TODO: use timestamps, to make sure queue update in FetchPlayer is consistent
        self._logged_off = self._prev_online_uuids - online_uuids  #
        self._logged_on = online_uuids - self._prev_online_uuids  #

        self._prev_online_uuids = online_uuids.copy()  #

        for uuid in self._logged_off:
            del self._logon_dt[uuid]

        for uuid in self._logged_on:
            self._logon_dt[uuid] = self._request_sqldt

    def get_logged_on(self) -> sUuid:
        return self._logged_on.copy()

    def get_request_timestamp(self) -> Timestamp:
        return self._request_timestamp

    def get_online_uuids(self) -> sUuid:
        return self._online_uuids.copy()
