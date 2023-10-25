from pprint import pprint
from time import perf_counter
from datetime import datetime
import asyncio
from request.request_wynncraft import RequestWynncraft
from request.request_uuid import RequestMojang
from database.vindicator_database import VindicatorDatabase
import mojang


class Test:
    def __init__(self):
        self.online_players = []
        self.online_usernames = []
        self.online_uuids = []
        self.request_wynn = RequestWynncraft()
        self.request_uuid = RequestMojang()

    async def main(self):
        t0 = perf_counter()
        print(1)
        await self.ainit()
        print(2)
        await self.get_online_players()
        print(3)
        await self.username_to_uuid()

        td = perf_counter() - t0
        print(f"Done in {td:.2f} seconds.")

    async def ainit(self):
        await VindicatorDatabase.ainit()
        await self.request_wynn.start()
        await self.request_uuid.start()

    async def get_online_players(self):
        self.online_players = await self.request_wynn.get_online_player_list()
        self.online_usernames = list(self.online_players["players"].keys())

    async def username_to_uuid(self):
        self.online_players = []
        print("FETCHING UUIDS")

        for username in self.online_usernames:
            uuid = self.request_uuid.get_uuid(username)
            self.online_uuids.append(uuid)
            print(f"{len(self.online_uuids)} UUIDS FETCHED")

    def print_results(self):
        print(f"DONE. FETCHED {len(self.online_players)} UUIDS")
        print(f"FETCHED {len(self.online_uuids)} UUIDS out of {len(self.online_players['onlinePlayers'])} ONLINE PLAYERS")


if __name__ == "__main__":
    asyncio.run(Test().main())
