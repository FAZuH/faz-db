import unittest

from loguru import logger

from kans.api import Api, WynnApi


class TestApi(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self._api: Api = WynnApi(logger)
        await self._api.start()

    async def test_guild(self) -> None:
        response = await self._api.guild.get("Avicia")
        self.assertIsNotNone(response.body)

    async def test_player(self) -> None:
        response = await self._api.player.get("Maarcus1")
        self.assertIsNotNone(response.body)

    async def test_players(self) -> None:
        response = await self._api.players.get()
        self.assertIsNotNone(response.body)

    async def asyncTearDown(self) -> None:
        await self._api.close()
