from datetime import datetime
import unittest

from fazdb.api import Api, WynnApi


class TestApiEndpointFromfixture(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self._api: Api = WynnApi()
        await self._api.start()

    async def test_guild_get(self) -> None:
        # ACTION
        response = await self._api.guild.get("Avicia")

        # ASSERT
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.name, "Avicia")
        self.assertAlmostEqual(
                response.headers.expires.to_datetime().timestamp(),
                datetime.now().timestamp(),
                delta=500
        )

    async def test_guild_prefix_get(self) -> None:
        response = await self._api.guild.get_from_prefix("AVO")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.prefix, "AVO")
        self.assertAlmostEqual(
                response.headers.expires.to_datetime().timestamp(),
                datetime.now().timestamp(),
                delta=500
        )

    async def test_player(self) -> None:
        response = await self._api.player.get_full_stats("FAZuH")
        self.assertIsNotNone(response.body)
        self.assertEqual(response.body.username, "FAZuH")
        self.assertAlmostEqual(
                response.headers.expires.to_datetime().timestamp(),
                datetime.now().timestamp(),
                delta=500
        )

    async def test_online_players(self) -> None:
        response = await self._api.player.get_online_uuids()
        self.assertIsNotNone(response.body)
        self.assertAlmostEqual(
                response.headers.expires.to_datetime().timestamp(),
                datetime.now().timestamp(),
                delta=500
        )

    async def asyncTearDown(self) -> None:
        await self._api.close()
