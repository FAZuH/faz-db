import json
import os

from fazdb.api.wynn.response import GuildResponse, OnlinePlayersResponse, PlayerResponse


class FixturesLoader:


    def __init__(self) -> None:
        self._online_players_fixture_fp = "tests/_fixtures/online_players.json"
        self._players_fixture_fp = "tests/_fixtures/players.json"
        self._guilds_fixture_fp = "tests/_fixtures/guilds.json"

    def get_online_uuids(self) -> OnlinePlayersResponse:
        self._online_uuids = None
        if os.path.exists(self._online_players_fixture_fp):
            with open(self._online_players_fixture_fp, 'r') as f:
                self._online_uuids = OnlinePlayersResponse(*(json.load(f)["0"]))

        if self._online_uuids is None:
            raise ValueError("No online players fixture found")
        return self._online_uuids

    def get_players(self) -> list[PlayerResponse]:
        self._player_stats = None
        if os.path.exists(self._players_fixture_fp):
            with open(self._players_fixture_fp, 'r') as f:
                self._player_stats = [PlayerResponse(*resp) for resp in json.load(f).values()]

        if self._player_stats is None:
             raise ValueError("No player stats fixture found")
        return self._player_stats

    def get_guilds(self) -> list[GuildResponse]:
        self._guild_stats = None
        if os.path.exists(self._guilds_fixture_fp):
            with open(self._guilds_fixture_fp, 'r') as f:
                self._guild_stats = [GuildResponse(*resp) for resp in json.load(f).values()]

        if self._guild_stats is None:
             raise ValueError("No guild stats fixture found")
        return self._guild_stats

    # async def response_to_mock(self) -> None:
    #     online_uuids: PlayersResponse = await self.get_online_uuids()
    #     with open(ONLINEUUIDS_MOCK_FP, "w") as f:
    #         json.dump({0: [online_uuids.body.raw, online_uuids.headers.raw]}, f, indent=4)

    #     online_player_stats: list[PlayerResponse] = await self.get_online_player_stats()
    #     to_dump_1 = {}
    #     for i, resp in enumerate(online_player_stats):
    #         to_dump_1[i] = [resp.body.raw, resp.headers.raw]
    #     with open(ONLINEPLAYERSTATS_MOCK_FP, "w") as f:
    #         json.dump(to_dump_1, f, indent=4)

    #     online_guild_stats: list[GuildResponse] = await self.get_online_guild_stats()
    #     to_dump_2 = {}
    #     for i, resp in enumerate(online_guild_stats):
    #         to_dump_2[i] = [resp.body.raw, resp.headers.raw]
    #     with open(ONLINEGUILDSTATS_MOCK_FP, "w") as f:
    #         json.dump(to_dump_2, f, indent=4)

    # async def mock_to_response(self) -> tuple[PlayersResponse, list[PlayerResponse], list[GuildResponse]]:
    #     # grab mock json from cache, and return it as a tuple of responses
    #     online_uuids = None
    #     online_player_stats = []
    #     online_guild_stats = []
    #     with open(ONLINEUUIDS_MOCK_FP, "r") as f:
    #         online_uuids = PlayersResponse(*json.load(f))

    #     with open(ONLINEPLAYERSTATS_MOCK_FP, "r") as f:
    #         for resp in json.load(f).values():
    #             online_player_stats.append(PlayerResponse(*resp))

    #     with open(ONLINEGUILDSTATS_MOCK_FP, "r") as f:
    #         for resp in json.load(f).values():
    #             online_guild_stats.append(GuildResponse(*resp))

    #     return online_uuids, online_player_stats, online_guild_stats

    # # @vcr.use_cassette
    # async def get_guild_stats(self, arg: str):
    #     return await self.wynnapi.get_guild_stats(arg)

    # # @vcr.use_cassette
    # async def get_online_uuids(self):
    #     return await self.wynnapi.get_online_uuids()

    # # @vcr.use_cassette
    # async def get_player_stats(self, arg: str):
    #     return await self.wynnapi.get_player_stats(arg)

    # async def get_online_player_stats(self):
    #     ret: list[PlayerResponse] = []
    #     concurrentRequests = 25
    #     onlineUuids: list[UsernameOrUuidField] = self.onlineUuids if self.onlineUuids else list((await self.get_online_uuids()).body.players)
    #     while onlineUuids:
    #         currentRequest: list[UsernameOrUuidField] = onlineUuids[:concurrentRequests]
    #         onlineUuids = onlineUuids[concurrentRequests:]
    #         ret.extend(await asyncio.gather(*[self.get_player_stats(uuid.username_or_uuid) for uuid in currentRequest]))
    #     self.onlinePlayerStats = ret
    #     return ret

    # async def get_online_guild_stats(self):
    #     ret: list[GuildResponse] = []
    #     concurrentRequests = 25
    #     onlinePlayerStats: list[PlayerResponse] = self.onlinePlayerStats or (await self.get_online_player_stats())
    #     onlineGuildNamesSet: Set[str] = set()
    #     for resp in onlinePlayerStats:
    #         if resp.body.guild:
    #             onlineGuildNamesSet.add(resp.body.guild.name)
    #     onlineGuildNames: list[str] = list(onlineGuildNamesSet)
    #     while onlineGuildNames:
    #         currentRequest: list[str] = onlineGuildNames[:concurrentRequests]
    #         onlineGuildNames = onlineGuildNames[concurrentRequests:]
    #         ret.extend(await asyncio.gather(*[self.get_guild_stats(guildName) for guildName in currentRequest]))
    #     self.onlineGuildStats = ret
    #     return ret
