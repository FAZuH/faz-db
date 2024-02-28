# pyright: reportPrivateUsage=false
from datetime import datetime
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock

from kans import Api, Database
from kans.api.wynn.response import OnlinePlayersResponse, PlayerResponse, GuildResponse
from kans.heartbeat.task import RequestList, ResponseList, TaskDbInsert


class TestTaskDbInsert(unittest.TestCase):

    def setUp(self) -> None:
        self._api = Mock(spec_set=Api)
        self._db = Mock(spec_set=Database)
        self._request_list = Mock(spec_set=RequestList)
        self._response_list = Mock(spec_set=ResponseList)
        self._task = TaskDbInsert(MagicMock(), self._api, self._db, self._request_list, self._response_list)

    def test_setup(self) -> None:
        # MOCKING
        self._db.create_all = AsyncMock()

        # ACTION
        self._task.setup()

        # ASSERTION
        self._db.create_all.assert_called_once()
        self._request_list.enqueue.assert_called_once_with(0, self._api.player.get_online_uuids())

    def test_run(self) -> None:
        # MOCKING
        self._task._run = AsyncMock()

        # ACTION
        self._task.run()

        # ASSERTION
        self._task._run.assert_called_once()

    async def test__run(self) -> None:
        # MOCKING
        self._response_list.get.return_value = None
        self._task._response_handler = Mock(spec_set=TaskDbInsert._ResponseHandler)
        online_players = Mock(spec_set=OnlinePlayersResponse)
        player = Mock(spec_set=PlayerResponse)
        guild = Mock(spec_set=GuildResponse)

        # ACTION
        await self._task._run()

        # ASSERTION
        self._db.kans_uptime_repository.insert.assert_called_once()
        self._task._response_handler.handle_onlineplayers_response.assert_not_called()
        self._task._response_handler.handle_player_response.assert_not_called()
        self._task._response_handler.handle_guild_response.assert_not_called()

        # MOCKING
        self._response_list.get.return_value = [online_players, player, guild]

        # ACTION
        await self._task._run()

        # ASSERTION
        self._task._response_handler.handle_onlineplayers_response.assert_called_once_with(online_players)
        self._task._response_handler.handle_player_response.assert_called_once_with(player)
        self._task._response_handler.handle_guild_response.assert_called_once_with(guild)
        self._db.kans_uptime_repository.insert.assert_called_once()
        self._db.online_players_repository.insert.assert_called_once()
        self._db.player_activity_history_repository.insert.assert_called_once()
        self._db.player_info_repository.insert.assert_called_once()
        self._db.character_info_repository.insert.assert_called_once()
        self._db.player_history_repository.insert.assert_called_once()
        self._db.character_history_repository.insert.assert_called_once()
        self._db.guild_info_repository.insert.assert_called_once()
        self._db.guild_history_repository.insert.assert_called_once()
        self._db.guild_member_history_repository.insert.assert_called_once()

    def test__insert_online_players_response(self) -> None:
        # TODO: Implement test
        # MOCKING
        # ACTION
        # ASSERTION
        pass

    def test__insert_player_responses(self) -> None:
        # TODO: Implement test
        # MOCKING
        # ACTION
        # ASSERTION
        pass

    def test__insert_guild_response(self) -> None:
        # TODO: Implement test
        # MOCKING
        # ACTION
        # ASSERTION
        pass


class TestResponseHandler(unittest.TestCase):

    def setUp(self) -> None:
        self._api = Mock(spec_set=Api)
        self.__request_list = Mock(spec_set=RequestList)
        self._manager = TaskDbInsert._ResponseHandler(self._api, self.__request_list)

    # OnlinePlayerResponse
    def test_process_new_response(self) -> None:
        # MOCKING
        uuid0 = "0"
        uuid1 = "1"
        uuid2 = "2"
        datetime0 = Mock(spec_set=datetime)
        datetime1 = Mock(spec_set=datetime)
        resp0 = MagicMock()
        resp1 = MagicMock()
        resp0.body.players = {uuid0, uuid1}
        resp0.headers.to_datetime.return_value = datetime0
        resp1.body.players = {uuid1, uuid2}
        resp1.headers.to_datetime.return_value = datetime1

        # ACTION
        self._manager._process_onlineplayers_response(resp0)

        # ASSERTION
        # NOTE: Assert that player 1 and 2 has logged on.
        self.assertSetEqual(self._manager.logged_on_players, {uuid0, uuid1})
        # NOTE: Assert that player 1 and 2 is online, with the correct logged on datetime.
        self.assertDictEqual(self._manager.online_players, {
                uuid0: datetime0,
                uuid1: datetime0
        })

        # ACTION
        self._manager._process_onlineplayers_response(resp1)

        # ASSERTION
        # NOTE: Assert that only player 2 has logged on because player 1 is already logged on.
        self.assertSetEqual(self._manager._logged_on_players, {uuid2})
        # NOTE: Assert that player 0 is no longer online, while player 1 and player 2 has the correct logged on datetime.
        self.assertDictEqual(self._manager.online_players, {
                uuid1: datetime0,
                uuid2: datetime1
        })

    def test_enqueue_player_stats(self) -> None:
        # MOCKING
        uuid0 = "player0"
        self._manager._logged_on_players = {uuid0}

        # ACTION
        self._manager._enqueue_player()

        # ASSERTION
        # NOTE: Assert that the correct player is being queued.
        self._api.player.get_full_stats.assert_called_once_with(uuid0)
        # NOTE: Assert that enqueue is called with the correct arguments.
        self.__request_list.enqueue.assert_called_once_with(0, self._api.player.get_full_stats())

    def test_requeueonline_players(self) -> None:
        # MOCKING
        resp = MagicMock()
        resp.headers.expires.to_datetime().timestamp.return_value = 69

        # ACTION
        self._manager._requeue_onlineplayers(resp)

        # ASSERTION
        # NOTE: Assert that enqueue is called with the correct arguments.
        self.__request_list.enqueue.assert_called_once_with(69, self._api.player.get_online_uuids(), priority=0)


    # PlayerResponse
    def test_process_player_response(self) -> None:
        # MOCKING
        guild0 = "guild0"
        guild1 = "guild1"
        uuid0 = "0"
        uuid1 = "1"
        uuid2 = "2"
        mock1 = MagicMock()
        mock2 = MagicMock()
        mock3 = MagicMock()
        mock1.body.guild.name = guild0
        mock1.body.uuid.uuid = uuid0
        mock1.body.online = True
        mock2.body.guild.name = guild0
        mock2.body.uuid.uuid = uuid1
        mock2.body.online = True
        mock3.body.guild.name = guild1
        mock3.body.uuid.uuid = uuid2
        mock3.body.online = True

        # ACTION
        self._manager._process_player_response([mock1])

        # ASSERTION
        # NOTE: Assert that guild "test0" is logged on.
        self.assertSetEqual(self._manager._logged_on_guilds, {guild0})
        # NOTE: Assert that guild "test0" is online with correct players.
        self.assertDictEqual(self._manager.online_guilds, {
                guild0: {uuid0}
        })

        # ACTION
        self._manager._process_player_response([mock2, mock3])

        # ASSERTION
        # NOTE: Assert that only guild test1 is logged on, because test0 is already logged on.
        self.assertSetEqual(self._manager._logged_on_guilds, {guild1})
        # NOTE: Assert that both guilds are online with correct players.
        self.assertDictEqual(self._manager.online_guilds, {
                guild0: {uuid0, uuid1},
                guild1: {uuid2}
        })

        # MOCKING
        mock3.body.online = False

        # ACTION
        self._manager._process_player_response([mock3])

        # ASSERTION
        # NOTE: Assert that guild test1 is no longer online.
        self.assertDictEqual(self._manager.online_guilds, {
                guild0: {uuid0, uuid1}
        })

    def test_enqueue_guild(self) -> None:
        # MOCKING
        guild0 = "guild0"
        self._manager._logged_on_guilds = {guild0}

        # ACTION
        self._manager._enqueue_guild()

        # ASSERTION
        # NOTE: Assert that the correct guild is being queued.
        self._api.guild.get.assert_called_once_with(guild0)
        # NOTE: Assert that enqueue is called with the correct arguments.
        self.__request_list.enqueue.assert_called_once_with(0, self._api.guild.get())

    def test_requeue_player(self) -> None:
        # MOCKING
        resp1 = MagicMock()
        resp2 = MagicMock()  # continued
        resp1.body.online = True
        resp1.headers.expires.to_datetime().timestamp.return_value = 69
        resp2.body.online = False

        # ACTION
        self._manager._requeue_player([resp2, resp1])

        # ASSERTION
        # NOTE: Assert that self._api.player.get_online_uuids() is called with the correct arguments
        self._api.player.get_full_stats.assert_called_once()
        # NOTE: Assert that enqueue is called with the correct arguments.
        self.__request_list.enqueue.assert_called_once_with(69 + 480, self._api.player.get_full_stats())


    # GuildResponse
    def test_requeue_guild(self) -> None:
        # MOCKING
        guild0 = "guild0"
        resp1 = MagicMock()
        resp2 = MagicMock()  # continued
        resp1.body.name = guild0
        resp1.body.members.get_online_members.return_value = 1
        resp1.headers.expires.to_datetime().timestamp.return_value = 69
        resp2.body.members.get_online_members.return_value = 0

        # ACTION
        self._manager._requeue_guild([resp1, resp2])

        # ASSERTION
        # NOTE: Assert that self._api.guild.get() is called with the correct arguments
        self._api.guild.get.assert_called_once_with(guild0)
        # NOTE: Assert that enqueue is called with the correct arguments.
        self.__request_list.enqueue.assert_called_once_with(69, self._api.guild.get())