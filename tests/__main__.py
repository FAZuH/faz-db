import asyncio
from tests.mock_wynnapi import MockWynnApi
# from vindicator import PlayersResponse


async def asyncrun() -> None:
    mockwynnapi = MockWynnApi()  # type: ignore
    from tests.test_wynndb_models import TestWynnDbModels
    t = TestWynnDbModels()
    await t.asyncSetUp()
    await t.test_guild_member_history()


if __name__ == "__main__":
    asyncio.run(asyncrun())
