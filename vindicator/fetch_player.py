from __future__ import annotations
from asyncio import create_task
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List
from uuid import UUID

from discord.ext.tasks import loop

from vindicator import (
    FetchOnline,
    PlayerCharacter,
    PlayerCharacterInfo,
    PlayerMain,
    PlayerMainInfo,
    VindicatorWebhook,
    WynncraftRequest,
    WynncraftResponseUtils
)
from vindicator.constants import *

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from vindicator.types import *


class FetchPlayer:

    _fetch_queue: Dict[UUID, Timestamp] = {}
    _fetched_players: lFetchedPlayers = []
    _latest_fetch: lFetchedPlayers = []
    _requeue_schedule: Dict[UUID, Timestamp] = {}

    @classmethod
    def get_latest_fetch(cls) -> lFetchedPlayers:
        return cls._latest_fetch.copy()

    @classmethod
    @loop(seconds=FETCH_PLAYER_INTERVAL)
    async def run(cls) -> None:
        t0: float = perf_counter()  # TODO: webhook logging

        cls._update_fetch_queue()
        if cls._fetch_queue:
            await cls._request_api()
            await cls._to_db()

    @classmethod
    def _update_fetch_queue(cls) -> None:
        """Modifies
        ---------
            - `cls._fetch_queue`
        """
        for uuid in FetchOnline.get_logged_on():  # Adds logged on into queue (if not already)
            if uuid not in cls._fetch_queue:
                cls._fetch_queue[uuid] = FetchOnline.get_online_req_timestamp()

        for uuid, requeue_time in cls._requeue_schedule.copy().items():  # Requeues fetched players (if passed schedule time)
            if uuid not in cls._fetch_queue and requeue_time <= time():
                cls._fetch_queue[uuid] = cls._requeue_schedule.pop(uuid)  # Requeue

    @classmethod
    async def _request_api(cls) -> None:
        """ Requests player stats from Wynncraft API. Saves into cls.fetched_guilds.

        Needs
        -----------
            - `cls._fetch_queue`

        Assigns
        -----------
            - `cls._latest_fetch`

        Clears
        -----------
            - `cls._fetch_queue`

        Modifies
        -----------
            - `cls._fetched_players`
            - `cls._requeue_schedule`
        """
        fetch_queue: Dict[UUID, float] = cls._fetch_queue.copy()
        uuids_to_fetch: lUuid = [uuid for uuid, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get UUIDS sorted by timestamp
        cls._fetch_queue.clear()  #
        cls._fetched_players.clear()  #

        concurrent_request: int = 50
        excs: List[BaseException] = []
        excs_: List[BaseException]
        resps: List[ClientResponse] = []
        resps_: List[ClientResponse]

        t0: float = perf_counter()
        # # test 100 players
        # uuids_to_fetch = uuids_to_fetch[:100]
        async with WynncraftRequest._rm.session as s:
            while uuids_to_fetch:
                excs_, resps_ = await WynncraftRequest.get_many_player_stats_response(s, uuids_to_fetch[:concurrent_request])
                uuids_to_fetch = uuids_to_fetch[concurrent_request:]  # Update queue
                excs.extend(excs_)
                resps.extend(resps_)

            for r in resps:
                resp_dt: float = WynncraftResponseUtils.parse_datestr1(r.headers.get("Date", ""))
                player_stat: PlayerStats = await r.json()

                cls._fetched_players.append({"response_timestamp": resp_dt, "player_stats": player_stat})
                cls._requeue_schedule[UUID(player_stat["uuid"])] = WynncraftResponseUtils.parse_datestr1(r.headers.get("Expires", ""))

        t1: float = perf_counter()
        create_task(VindicatorWebhook.log("wynncraft_request", "request", {
            "fetched players": len(resps),
            "time spent": f"{t1-t0:.2f}s",
            "exceptions": len(excs),
        }, title="Fetch online player stats"))
        cls._latest_fetch = cls._fetched_players.copy()

    @classmethod
    async def _to_db(cls) -> None:
        """Saves fetched players data into database.

        Needs
        -----------
            - `cls._fetched_players`
        """
        fetched_players: lFetchedPlayers = cls._latest_fetch.copy()
        t0: float = perf_counter()
        await PlayerMainInfo.to_db(fetched_players); t1: float = perf_counter()
        await PlayerCharacterInfo.to_db(fetched_players); t2: float = perf_counter()
        await PlayerMain.to_db(fetched_players); t3: float = perf_counter()
        await PlayerCharacter.to_db(fetched_players); t4: float = perf_counter()

        create_task(VindicatorWebhook.log("database", "write", {
            "records": len(cls._fetched_players),
            "table1": PLAYER_MAIN_INFO,
            "time1": f"{t1-t0:.2f}s",
            "table2": PLAYER_CHARACTER_INFO,
            "time2": f"{t2-t1:.2f}s",
            "table3": PLAYER_MAIN,
            "time3": f"{t3-t2:.2f}s",
            "table4": PLAYER_CHARACTER,
            "time4": f"{t4-t3:.2f}s",
        }, title="Save fetched players to database"))
