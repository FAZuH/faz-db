import asyncio
from datetime import datetime
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List, Set
from uuid import UUID

from discord import Webhook
from discord.ext.tasks import loop
import mojang

from database.vindicator_database import VindicatorDatabase
from request.request_wynncraft import RequestWynncraft, WynncraftResponseUtils
from settings import FETCH_ONLINE_INTERVAL, FETCH_PLAYER_INTERVAL, FETCH_ONLINE_WEBHOOK, FETCH_PLAYER_WEBHOOK, VindicatorTables

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from typeddict.wynncraft_response import OnlinePlayerList, PlayerStats


class FetchPlayer:

    _raw_online_player_list: "OnlinePlayerList" = {}
    _latest_fetch: Dict[int, "PlayerStats"] = {}

    def __init__(self) -> None:
        self.fetch_queue: Dict[str, int] = {}
        self.fetched_players: List[dict] = []
        self.fetching: bool = False
        self.flagged_uuids: Set[UUID] = set()
        self.logoffs: Set[str] = set()
        self.logons: Set[str] = set()
        self.logon_timestamps: Dict[str, int] = {}
        self.mojang_api = mojang.API()
        self.online_player_count: int = 0
        self.online_usernames: Set[str] = set()
        self.online_uuids: Set[UUID] = set()
        self.previous_online_uuids: Set[UUID] = set()
        self.requeue_schedule: Dict[str, int] = {}
        self.request_wynncraft: RequestWynncraft = RequestWynncraft()
        self.fonline_webhook: Webhook = Webhook.from_url(FETCH_ONLINE_WEBHOOK)
        self.fplayer_webhook: Webhook = Webhook.from_url(FETCH_PLAYER_WEBHOOK)

    async def ainit(self) -> None:
        return

    @loop(seconds=FETCH_ONLINE_INTERVAL)
    async def run(self) -> None:
        t0 = perf_counter()

        try:
            await self.fetch_api()  # TODO: Need testing
            await self.username_to_uuid()  # TODO: Need testing
            await self.update_online_info()  # TODO: Need testing
            await self.update_fetch_queue()  # TODO: Need testing

            if not self.fetching:
                await self.fetch_players()  # TODO: Need testing
                await self.to_db()  # TODO: Need testing

        except Exception as e:
            # TODO: Handle Error, Attempt retry
            # TODO: Send error to webhook
            pass

        td = perf_counter - t0

    async def fetch_api(self) -> None:
        self.raw_online_player_list = await self.request_wynncraft.get_online_player_list()  #
        self.online_usernames = set(self.raw_online_player_list["players"].keys())  #
        self.online_player_count = self.raw_online_player_list["onlinePlayers"]  #

    async def username_to_uuid(self) -> None:
        lookup_in_mojang: List[str] = []
        online_uuids: Set[str] = set()

        for username in self.online_usernames.copy():
            # Look up UUID in database
            params = {'username': username}
            query = f"SELECT uuid FROM {VindicatorTables.PLAYER_MAIN_INFO} WHERE latest_username = :username"
            uuid = await VindicatorDatabase.read_all(query=query, params=params)

            # If not in database (player has never been seen before)
            if uuid is None:
                lookup_in_mojang.append(username)
                continue

            online_uuids.add(UUID(uuid))

        n = 10
        # Requests 10 UUIDs at a time
        while lookup_in_mojang:
            try:
                get_uuids_task = asyncio.create_task(self.mojang_api.get_uuids(lookup_in_mojang[:n]))
                uuids: Dict[str, str] = await get_uuids_task

            except mojang.TooManyRequests:
                break  # TODO: Cannot afford to wait longer, need to find a way to handle this
                # await asyncio.sleep(60)

            uuids = set(map(UUID, uuids.values()))
            online_uuids.update(uuids.values())
            lookup_in_mojang = lookup_in_mojang[n:]

        self.online_uuids = online_uuids

    async def update_online_info(self) -> None:
        self.timestamp = int(time())

        online_uuids = self.online_uuids.copy()

        self.logons = online_uuids - self.previous_online_uuids  #
        self.logoffs = self.previous_online_uuids - online_uuids  #

        self.previous_online_uuids = online_uuids.copy()  #

        for uuid in self.logoffs:
            del self.logon_timestamps[uuid]

        for uuid in self.logons:
            self.logon_timestamps[uuid] = self.timestamp

    async def update_fetch_queue(self) -> None:
        # Adds logged on into queue (if not already)
        for uuid in self.logons.copy():
            if uuid in self.fetch_queue:
                continue

            self.fetch_queue[uuid] = self.timestamp

        # Requeues fetched players (if passed schedule time)
        for uuid, requeue_time in self.requeue_schedule.copy().items():
            if uuid in self.fetch_queue:
                continue

            # Requeue
            if requeue_time < time():
                self.fetch_queue[uuid] = self.requeue_schedule.pop(uuid)

    async def fetch_players(self) -> None:
        fetch_queue = self.fetch_queue.copy()
        self.fetch_queue.clear()  #
        self.fetched_players.clear()  #
        uuids_to_fetch = dict(sorted(fetch_queue.items(), key=lambda item: item[1]))  # Sort by timestamp

        self.fetching = True
        for uuid in uuids_to_fetch:
            if uuid not in self.online_uuids:
                continue  # Player might have logged off while in queue

            try:
                player_stat_resp: "ClientResponse" = await self.request_wynncraft.get_player_stats(uuid, json_response=False)

            except Exception as e:
                # TODO: Send error to webhook
                continue

            player_stat: "PlayerStats" = await player_stat_resp.json()
            self.fetched_players.append(player_stat)

            self.requeue_schedule[player_stat.uuid] = WynncraftResponseUtils.parse_datestr(player_stat_resp["Date"])
            self.requeue_schedule[player_stat.uuid] += 120 if uuid in self.flagged_uuids else 600

        self.fetching = False

    async def to_db(self) -> None:
        # TODO: Add to databases:
        # - player_character
        # - player_character_info
        # - player_main
        # - player_main_info
        # - player_uptime
        # - raw_latest_others: online_player_list
        # - raw_online_player
        # - raw_recent_player
        return

    @property
    def raw_online_player_list(self) -> "OnlinePlayerList":
        return FetchPlayer._raw_online_player_list

    @raw_online_player_list.setter
    def raw_online_player_list(self, value: "OnlinePlayerList") -> None:
        FetchPlayer._raw_online_player_list = value
