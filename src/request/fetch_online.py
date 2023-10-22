from time import perf_counter, time
from typing import Dict, Literal, Set, Union

from discord import Webhook
from discord.ext.tasks import loop

from request.request import Request
from settings import FETCH_ONLINE_INTERVAL, FETCH_ONLINE_WEBHOOK

OnlinePlayerList = Dict[Literal["onlinePlayers", "players"], Union[Dict[str, str], int]]


class FetchOnline:
    online_players: Dict[str, str] = {}

    def __init__(self) -> None:
        self.logon_timestamps: Dict[str, int] = {}
        self.online_usernames: Set[str] = set()
        self.previous_online_usernames: Set[str] = set()
        self.webhook: Webhook = Webhook.from_url(FETCH_ONLINE_WEBHOOK)

    @loop(seconds=FETCH_ONLINE_INTERVAL)
    async def run(self) -> None:
        t0 = perf_counter()

        try:
            await self.update_online_info()

        except Exception as e:
            self.webhook.send()

        td = perf_counter - t0

    async def update_online_info(self):
        FetchOnline.online_players: Dict[str, str] = await Request.get_online_players()["players"]
        self.timestamp = round(time())

        self.online_usernames = set(FetchOnline.online_players.keys())

        self.logons = self.online_usernames - self.previous_online_usernames
        self.logoffs = self.previous_online_usernames - self.online_usernames

        self.previous_online_usernames = self.online_usernames.copy()

        for username in self.logoffs:
            del self.logon_timestamps[username]

        for username in self.logons:
            self.logon_timestamps[username] = self.timestamp

    async def convert_data(self):
        return
