import asyncio
from datetime import datetime
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List, Set, Tuple, TypedDict
from uuid import UUID

from discord import Webhook
from discord.ext.tasks import loop
from mojang import API, TooManyRequests
from database.vindicator_database import VindicatorDatabase
from objects.vindicator_database import (
    PlayerCharacter,
    PlayerCharacterInfo,
    PlayerMain,
    PlayerMainInfo,
    PlayerUptime,
    RawLatestOthers,
    RawOnlinePlayer,
    RawRecentPlayer,
)
from request.wynncraft_api_request import WynncraftAPIRequest
from settings import (
    FETCH_ONLINE_INTERVAL,
    FETCH_PLAYER_INTERVAL,
    VindicatorTables
)
from webhook.vindicator_webhook import VindicatorWebhook
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from objects.wynncraft_response import OnlinePlayerList, PlayerStats


FetchedPlayer = TypedDict("FetchedPlayer", {"response_datetime": float, "player_stats": "PlayerStats"})

class FetchPlayer:

    _raw_online_player_list: "OnlinePlayerList"
    _latest_fetch: List[FetchedPlayer] = []

    fetch_queue: Dict[UUID, float] = {}
    fetched_players: List[FetchedPlayer] = []
    fetching: bool = False
    flagged_uuids: Set[UUID] = set()  # TODO: Implement this on a later stage
    logoffs: Set[UUID] = set()
    logons: Set[UUID] = set()
    logon_timestamps: Dict[UUID, float] = {}
    mojang_api: API = API()
    online_player_count: int
    online_usernames: Set[str] = set()
    online_uuids: Set[UUID] = set()
    previous_online_uuids: Set[UUID] = set()
    requeue_schedule: Dict[UUID, float] = {}
    timestamp: float
    usernames_not_in_anywhere: Set[str] = set()

    @classmethod
    @loop(seconds=FETCH_ONLINE_INTERVAL)
    async def run(cls) -> None:
        print("self.fetch_api()")
        await cls._request_api()
        print("self.username_to_uuid()")
        await cls._username_to_uuid()
        print("self.update_online_info()")
        await cls._update_online_info()
        print("self.update_fetch_queue()")
        await cls._update_fetch_queue()

        if not cls.fetching:
            print("self.fetch_players()")
            await cls._fetch_players()  # TODO: Need testing
            print("self.to_db()")
            await cls._to_db()  # TODO: Need testing

    @classmethod
    async def _request_api(cls) -> None:
        """ Gets self.raw_online_player_list, self.online_usernames, self.online_player_count """
        cls.raw_online_player_list = await WynncraftAPIRequest.get_online_player_json()
        cls.timestamp = time()  #
        cls.online_usernames = set(cls.raw_online_player_list["players"].keys())  #
        cls.online_player_count = cls.raw_online_player_list["total"]  #

    @classmethod
    async def _username_to_uuid(cls) -> None:
        """ Gets self.online_uuids, self.usernames_not_in_anywhere """
        usernames: Set[str] = cls.online_usernames.copy()
        params: Dict[str, Set[str]] = {'usernames': usernames}
        query: str = f"SELECT latest_username, uuid FROM {VindicatorTables.PLAYER_MAIN_INFO} WHERE latest_username IN %(usernames)s"
        result = await VindicatorDatabase.read_all(query=query, params=params)  # TODO: TypedDict this

        online_uuids: Set[UUID] = {UUID(bytes=d["uuid"]) for d in result}
        usernames_not_in_db: List[str] = list(usernames - {d["latest_username"] for d in result})

        temp: Set[str] = set(usernames_not_in_db.copy())

        n = 10
        # Requests 10 UUIDs at a time
        while usernames_not_in_db:
            try:
                uuids: Dict[str, str] = await asyncio.get_event_loop() \
                    .run_in_executor(None, cls.mojang_api.get_uuids, usernames_not_in_db[:n])

            except TooManyRequests:
                print("mojang.TooManyRequests")
                break  # TODO: Cannot afford to wait longer, need to find a way to handle this
                # await asyncio.sleep(60)

            temp = temp - {username for username in uuids}

            online_uuids.update(set(map(UUID, uuids.values())))
            usernames_not_in_db = usernames_not_in_db[n:]

        cls.usernames_not_in_anywhere = temp.copy()
        cls.online_uuids = online_uuids.copy()  #
        print("len self.usernames_not_in_anywhere: ", len(cls.usernames_not_in_anywhere))
        print("len self.online_uuids: ", len(cls.online_uuids))

    @classmethod
    async def _update_online_info(cls) -> None:
        """ Gets self.logons, self.logoffs, self.previous_online_uuids. Updates self.logon_timestamps"""
        online_uuids: Set[UUID] = cls.online_uuids.copy()

        cls.logons: Set[UUID] = online_uuids - cls.previous_online_uuids  #
        cls.logoffs: Set[UUID] = cls.previous_online_uuids - online_uuids  #

        cls.previous_online_uuids: Set[UUID] = online_uuids.copy()  #

        for uuid in cls.logoffs:
            del cls.logon_timestamps[uuid]

        for uuid in cls.logons:
            cls.logon_timestamps[uuid] = cls.timestamp

    @classmethod
    async def _update_fetch_queue(cls) -> None:
        """ Updates self.fetch_queue """
        # Adds logged on into queue (if not already)
        for uuid in cls.logons.copy():
            if uuid in cls.fetch_queue:
                continue

            cls.fetch_queue[uuid] = cls.timestamp

        # Requeues fetched players (if passed schedule time)
        for uuid, requeue_time in cls.requeue_schedule.copy().items():
            if uuid in cls.fetch_queue or requeue_time > time():
                continue

            cls.fetch_queue[uuid] = cls.requeue_schedule.pop(uuid)  # Requeue

    @classmethod
    async def _fetch_players(cls) -> None:
        """Requests player stats from Wynncraft API. Saves into cls.fetched_guilds

        Guilds-to-fetch are grabbed from:
        - _latest_fetch class variable of FetchPlayer class
        - guilds that's not saved in database
        """
        fetch_queue: Dict[UUID, float] = cls.fetch_queue.copy()
        cls.fetch_queue.clear()  #
        cls.fetched_players.clear()  #
        uuids_to_fetch: List[UUID] = [uuid for uuid, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get UUIDS sorted by timestamp

        cls.fetching = True
        while uuids_to_fetch:
            concurrent_request: int = 275
            uuids_to_fetch_ = uuids_to_fetch[:concurrent_request]  # Poll
            uuids_to_fetch = uuids_to_fetch[concurrent_request:]  # Update queue

            player_stat_resps: List["ClientResponse"] = await WynncraftAPIRequest.get_many_player_stats_response(uuids_to_fetch_)

            for response in player_stat_resps:
                response_dt: float = WynnUtils.parse_datestr1(response.headers.get("Date", ""))

                player_stat: "PlayerStats" = await response.json()
                player_uuid: UUID = UUID(player_stat["uuid"])
                cls.fetched_players.append({"response_datetime": response_dt, "player_stats": player_stat})

                cls.requeue_schedule[player_uuid] = response_dt + (120 if player_uuid in cls.flagged_uuids else 600)

        cls._latest_fetch = cls.fetched_players.copy()
        cls.fetching = False

    @classmethod
    async def _to_db(cls) -> None:
        ################################################################################################################
        import json
        with open("onlineplayers11.4.23-2.21am.json") as f:
            cls.fetched_players = json.load(f)
        ################################################################################################################

        player_character = PlayerCharacter.from_raw(cls.fetched_players)
        player_character_info = PlayerCharacterInfo.from_raw(cls.fetched_players)
        player_main = PlayerMain.from_raw(cls.fetched_players)
        player_main_info = PlayerMainInfo.from_raw(cls.fetched_players)
        # TODO: Add to databases. Figure out a way to do these
        # - player_uptime
        # - raw_latest_others: online_player_list
        # - raw_online_player
        # - raw_recent_player

        await PlayerMainInfo.to_db(player_main_info)
        await PlayerCharacterInfo.to_db(player_character_info)
        await PlayerMain.to_db(player_main)
        await PlayerCharacter.to_db(player_character)
