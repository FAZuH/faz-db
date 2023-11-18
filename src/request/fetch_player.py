import asyncio
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List, Set, TypeAlias, TypedDict
from uuid import UUID

from discord.ext.tasks import loop
from loguru import logger
from objects.database import (
    PlayerCharacter,
    PlayerCharacterInfo,
    PlayerMain,
    PlayerMainInfo,
)

from .fetch_online import FetchOnline
from constants import FETCH_PLAYER_INTERVAL
from database.vindicator_database import VindicatorDatabase
from src.request.wynncraft_request import WynncraftRequest
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils
from webhook.vindicator_webhook import VindicatorWebhook

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from objects.wynncraft_response import PlayerStats

FetchedPlayer = TypedDict("FetchedPlayer", {"response_timestamp": float, "player_stats": "PlayerStats"})

Timestamp: TypeAlias = float
Username: TypeAlias = str
Uuid: TypeAlias = UUID

lFetchedPlayers: TypeAlias = List[FetchedPlayer]
lUsernames: TypeAlias = List[Username]
lUuids: TypeAlias = List[Uuid]
sUsernames: TypeAlias = Set[Username]
sUuids: TypeAlias = Set[Uuid]


class FetchPlayer:

    latest_fetch: lFetchedPlayers = []

    def __init__(self) -> None:
        self._fetch_queue: Dict[UUID, Timestamp] = {}
        self._fetched_players: lFetchedPlayers = []
        self._fetching: bool = False
        self._flagged_uuids: sUuids = set()  # TODO: Implement later
        self._requeue_schedule: Dict[UUID, Timestamp] = {}

        self.request: WynncraftRequest = WynncraftRequest()
        return

    @loop(seconds=FETCH_PLAYER_INTERVAL)
    async def loop_run(self) -> None:
        asyncio.create_task(self.run())
        return

    async def run(self) -> None:
        self._update_fetch_queue()
        if not self._fetching and self._fetch_queue:
            t0: float = perf_counter()
            logger.info(f"Running loop")

            await asyncio.sleep(0.0)
            await self._fetch_players()
            await self._to_db()
            await VindicatorWebhook.send("fetch_player", "success", f"**latest_fetched**={len(self._fetched_players)}:t={perf_counter()-t0:.2f} ")
        return

    def _update_fetch_queue(self) -> None:
        """Modifies
        ---------
            - `self._fetch_queue`
        """
        for uuid in FetchOnline.logons.copy():  # Adds logged on into queue (if not already)
            if uuid not in self._fetch_queue:
                self._fetch_queue[uuid] = FetchOnline._timestamp

        for uuid, requeue_time in self._requeue_schedule.copy().items():  # Requeues fetched players (if passed schedule time)
            if uuid not in self._fetch_queue and requeue_time <= time():
                self._fetch_queue[uuid] = self._requeue_schedule.pop(uuid)  # Requeue
        return

    async def _fetch_players(self) -> None:
        """Requests player stats from Wynncraft API. Saves into self.fetched_guilds.

        Guilds-to-fetch are grabbed from:
        - latest_fetch class variable of FetchPlayer class
        - guilds that's not saved in database

        Needs
        -----------
            - `self._fetch_queue`

        Assigns
        -----------
            - `FetchPlayer.latest_fetch`

        Clears
        -----------
            - `self._fetch_queue`

        Modifies
        -----------
            - `self._fetched_players`
            - `self._requeue_schedule`
        """
        fetch_queue: Dict[UUID, float] = self._fetch_queue.copy()
        self._fetch_queue.clear()  #
        self._fetched_players.clear()  #
        uuids_to_fetch: lUuids = [uuid for uuid, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get UUIDS sorted by timestamp

        concurrent_request: int = 50
        invalid_uuids: List[BaseException] = []
        exceptions_: List[BaseException]
        usernames_nowhere: List[BaseException] = []
        responses: List["ClientResponse"] = []
        responses_: List["ClientResponse"]

        self._fetching = True
        logger.info(f"uuids_to_fetch={len(uuids_to_fetch)}")
        t0: float = perf_counter()

        while uuids_to_fetch:
            exceptions_, responses_ = await self.request.get_many_player_stats_response(uuids_to_fetch[:concurrent_request])
            uuids_to_fetch = uuids_to_fetch[concurrent_request:]  # Update queue
            invalid_uuids.extend(exceptions_)
            responses.extend(responses_)

        while FetchOnline.usernames_nowhere:
            exceptions_, responses_ = await self.request.get_many_player_stats_response(FetchOnline.usernames_nowhere[:concurrent_request])
            FetchOnline.usernames_nowhere = FetchOnline.usernames_nowhere[concurrent_request:]
            usernames_nowhere.extend(exceptions_)
            responses.extend(responses_)

        for response in responses:
            response_dt: float = WynnUtils.parse_datestr1(response.headers.get("Expires", "")) - float(response.headers.get("Cache-Control", "_=0").split('=')[-1])
            player_stat: "PlayerStats" = await response.json()
            player_uuid: UUID = UUID(player_stat["uuid"])
            self._fetched_players.append({"response_timestamp": response_dt, "player_stats": player_stat})
            self._requeue_schedule[player_uuid] = response_dt + (120.0 if player_uuid in self._flagged_uuids else 600.0)

        await VindicatorWebhook.send("fetch_player", "info",
            f"**player_stat_resps**={len(responses)}\n"
            f"**fetched_players**={len(self._fetched_players)}\n"
            f"**invalid_uuids**={len(invalid_uuids)}\n"
            f"**usernames_nowhere**={len(usernames_nowhere)}"
            f"**t**={perf_counter()-t0:.2f}"
        )
        FetchPlayer.latest_fetch = self._fetched_players.copy()
        self._fetching = False
        return

    async def _to_db(self) -> None:
        """Saves fetched players data into database.

        Needs
        -----------
            - `self._fetched_players`
        """
        # with open("C:/Users/user/VSCodeProjects/Vindicator/tests/fetched_player.json") as f:
        #     import json
        #     self._fetched_players = json.load(f)

        await PlayerMainInfo.to_db(self._fetched_players)
        await PlayerCharacterInfo.to_db(self._fetched_players)
        await PlayerMain.to_db(self._fetched_players)
        await PlayerCharacter.to_db(self._fetched_players)
        # TODO: raw_latest_others: online_player_list
        return
