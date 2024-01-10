from __future__ import annotations
from asyncio import create_task, gather
from uuid import UUID

from discord.ext.tasks import loop

from vindicator import (
    Logger,
    PlayerActivityUtil,
    PlayerServerUtil,
    WynncraftRequest,
    WynncraftResponseUtil
)
from vindicator.constants import *
from vindicator.typehints import *


class FetchOnline:

    _logged_off: sUuid = set()
    _logged_on: sUuid = set()  # used in FetchPlayer
    _logon_dt: Dict[UUID, str] = {}
    _request_timestamp: Timestamp
    _online_uuids: sUuid = set()  # used in FetchPlayer
    _prev_online_uuids: sUuid = set()
    _raw_online_uuids: OnlinePlayerList


    @classmethod
    def get_logged_on(cls) -> sUuid:
        return cls._logged_on.copy()

    @classmethod
    def get_request_timestamp(cls) -> Timestamp:
        return cls._request_timestamp

    @classmethod
    def get_online_uuids(cls) -> sUuid:
        return cls._online_uuids.copy()


    @classmethod
    @loop(seconds=FETCH_ONLINE_INTERVAL)
    @Logger.logging_decorator
    async def run(cls) -> None:
        await cls._request_api()
        task1: Task = create_task(PlayerServerUtil(cls._raw_online_uuids).to_db())
        cls._update_online_info()
        task2: Task = create_task(PlayerActivityUtil(cls._request_sqldt, cls._logon_dt).to_db())
        await gather(task1, task2)

    @classmethod
    @Logger.logging_decorator
    async def _request_api(cls) -> None:
        """ Assigns
        -----------
            - `_raw_online_uuids`
            - `_online_uuids`
            - `_request_sqldt`
            - `_request_timestamp`
        """
        async with WynncraftRequest() as client:
            res = await WynncraftRequest.get_online_uuids(client)
            cls._raw_online_uuids = res.json
            cls._online_uuids = {UUID(uuid) for uuid in res.json["players"]}
            cls._request_sqldt: str = WynncraftResponseUtil.resp_to_sqldt(res.headers.get("Date", ""))
            cls._request_timestamp = WynncraftResponseUtil.resp_to_timestamp(res.headers.get("Date", ""))

    @classmethod
    def _update_online_info(cls) -> None:
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
        online_uuids: sUuid = cls._online_uuids.copy()

        # TODO: use timestamps, to make sure queue update in FetchPlayer is consistent
        cls._logged_off = cls._prev_online_uuids - online_uuids  #
        cls._logged_on = online_uuids - cls._prev_online_uuids  #

        cls._prev_online_uuids = online_uuids.copy()  #

        for uuid in cls._logged_off:
            del cls._logon_dt[uuid]

        for uuid in cls._logged_on:
            cls._logon_dt[uuid] = cls._request_sqldt
