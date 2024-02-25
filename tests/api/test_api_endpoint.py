import unittest

from loguru import logger

from kans.api import Api, WynnApi


class TestApiEndpoint(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self._api: Api = WynnApi(logger)
        await self._api.start()

    async def test_guild_get(self) -> None:
        response = await self._api.guild.get("Avicia")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.name, "Avicia")

    async def test_guild_prefix_get(self) -> None:
        response = await self._api.guild.get_from_prefix("AVO")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.prefix, "AVO")

    async def test_player(self) -> None:
        response = await self._api.player.get_full_stats("FAZuH")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.username, "FAZuH")

    async def test_online_players(self) -> None:
        response = await self._api.player.get_online_uuids()
        self.assertIsNotNone(response.body)

    async def asyncTearDown(self) -> None:
        await self._api.close()
