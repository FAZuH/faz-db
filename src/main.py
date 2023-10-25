import asyncio

from .database.vindicator_database import VindicatorDatabase
from .request.request_wynncraft import RequestWynncraft


class Main:
    def __init__(self) -> None:
        pass

    async def main(self) -> None:
        pass

    async def ainit(self) -> None:
        pass

    async def start(self) -> None:
        await VindicatorDatabase.ainit()
        await RequestWynncraft.ainit()


if __name__ == "__main__":
    asyncio.run(Main().main())
