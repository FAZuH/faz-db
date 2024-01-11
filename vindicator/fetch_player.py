from __future__ import annotations
from asyncio import create_task, TaskGroup
from time import time
from uuid import UUID

from discord.ext.tasks import loop

from vindicator import (
    FetchOnline,
    Logger,
    PlayerCharacterUtil,
    PlayerCharacterInfoUtil,
    PlayerMainUtil,
    PlayerMainInfoUtil,
    WynncraftRequest,
    WynncraftResponseUtil
)
from vindicator.constants import *
from vindicator.typehints import *


class FetchPlayer:

    _fetch_queue: Dict[UUID, Timestamp] = {}
    _latest_fetch: List[FetchedPlayer] = []
    _requeue_schedule: Dict[UUID, Timestamp] = {}
    _is_running: bool = False


    @classmethod
    @loop(seconds=FETCH_PLAYER_INTERVAL)
    async def run(cls) -> None:
        if not cls._is_running:
            create_task(cls._run())

    @classmethod
    @Logger.logging_decorator
    async def _run(cls) -> None:
        cls._is_running = True
        cls._update_fetch_queue()
        if cls._fetch_queue:
            await cls._fetch_players()
            await cls._to_db()
        cls._is_running = False


    @classmethod
    def _update_fetch_queue(cls) -> None:
        """Modifies
        ---------
            - `_fetch_queue`
        """
        for uuid in FetchOnline.get_logged_on():  # Adds logged on into queue (if not already)
            if uuid not in cls._fetch_queue:
                cls._fetch_queue[uuid] = FetchOnline.get_request_timestamp()

        for uuid, requeue_time in cls._requeue_schedule.copy().items():  # Requeues fetched players (if passed schedule time)
            if uuid not in cls._fetch_queue and requeue_time <= time():
                cls._fetch_queue[uuid] = cls._requeue_schedule.pop(uuid)  # Requeue

    @classmethod
    @Logger.logging_decorator
    async def _fetch_players(cls) -> None:
        """ Requests player stats from Wynncraft API. Saves into cls.fetched_guilds.

        Needs
        -----------
            - `_fetch_queue`

        Assigns
        -----------
            - `_latest_fetch`

        Clears
        -----------
            - `_fetch_queue`

        Modifies
        -----------
            - `_requeue_schedule`
        """
        fetched_players: List[FetchedPlayer] = []
        fetch_queue: Dict[UUID, float] = cls._fetch_queue.copy()
        uuids_to_fetch: lUuid = [uuid for uuid, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get UUIDS sorted by timestamp
        cls._fetch_queue.clear()  #

        concurrent_request: int = 50
        excs: List[BaseException] = []
        excs_: List[BaseException]
        ress: List[ResponseSet[PlayerStats, Headers]] = []
        ress_: List[ResponseSet[PlayerStats, Headers]]

        async with WynncraftRequest() as client:
            while uuids_to_fetch:
                excs_, ress_ = await client.get_many_player_stats(uuids_to_fetch[:concurrent_request])
                uuids_to_fetch = uuids_to_fetch[concurrent_request:]  # Dequeue
                excs.extend(excs_)
                ress.extend(ress_)

        for r in ress:
            fetched_players.append({"resp_datetime": WynncraftResponseUtil.resp_to_sqldt(r.headers.get("Date", "")), "player_stats": r.json})
            cls._requeue_schedule[UUID(r.json["uuid"])] = WynncraftResponseUtil.resp_to_timestamp(r.headers.get("Expires", ""))

        cls._latest_fetch = fetched_players.copy()

    @classmethod
    async def _to_db(cls) -> None:
        """Saves fetched players data into database.

        Needs
        -----------
            - `_fetched_players`
        """
        fetched_players: List[FetchedPlayer] = cls.get_latest_fetch()
        async with TaskGroup() as tg:
            tg.create_task(PlayerMainInfoUtil(fetched_players).to_db())
            tg.create_task(PlayerCharacterInfoUtil(fetched_players).to_db())
            tg.create_task(PlayerMainUtil(fetched_players).to_db())
            tg.create_task(PlayerCharacterUtil(fetched_players).to_db())


    @classmethod
    def get_latest_fetch(cls) -> List[FetchedPlayer]:
        return cls._latest_fetch.copy()
