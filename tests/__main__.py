import asyncio
from tests.mock_wynnapi import MockWynnApi
# from vindicator import PlayersResponse


async def asyncrun() -> None:
    mockwynnapi = MockWynnApi()  # type: ignore
    from tests.test_wynndb_repository import TestWynnDbRepository
    t = TestWynnDbRepository()
    await t.asyncSetUp()
    await t.test_character_history_repo()


if __name__ == "__main__":
    asyncio.run(asyncrun())
