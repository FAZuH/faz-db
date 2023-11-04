import asyncio

from database.vindicator_database import VindicatorDatabase
from request.fetch_guild import FetchGuild
from request.fetch_player import FetchPlayer
from request.wynncraft_api_request import WynncraftAPIRequest

from objects.vindicator_database import *


class Main:
    def __init__(self) -> None:
        pass

    async def main(self) -> None:
        pass

    async def ainit(self) -> None:
        pass


########################################################################################################################

from time import perf_counter
from pprint import pprint
from dataclasses import asdict

class Test:

    @staticmethod
    async def ainit() -> None:
        await VindicatorDatabase.ainit()
        await WynncraftAPIRequest.ainit()

    @staticmethod
    async def main() -> None:
        await Test.ainit()
        await FetchGuild.run()

if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(Test.main())
    td = perf_counter() - t0
    print(f"Time elapsed: {td:0.4f} seconds", "DONE", sep="\n")

########################################################################################################################
