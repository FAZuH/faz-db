import unittest
from unittest.mock import AsyncMock, MagicMock

from fazdb.heartbeat.task.task_api_request import TaskApiRequest


class TestTaskApiRequest(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.api = MagicMock()
        self.request_list = MagicMock()
        self.response_list = MagicMock()
        self.task = TaskApiRequest(self.api, self.request_list, self.response_list)

    @unittest.skip("not ready")
    async def test_setup(self):
        self.task.setup()
        self.api.start.assert_called_once()

    def test_teardown(self):
        self.api.close = AsyncMock()
        self.task.teardown()
        self.api.close.assert_called_once()

    def test_run(self):
        self.task._run = AsyncMock()
        self.task.run()
        self.task._run.assert_called_once()
        self.assertIsNotNone(self.task._latest_run)

    async def test_check_api_session(self):
        self.api.request.is_open.return_value = False
        self.task._api.start = AsyncMock()
        await self.task._check_api_session()
        self.api.start.assert_called_once()

    @unittest.skip("not ready")
    async def test_start_requests(self):
        # PREPARE
        self.task._request_list = MagicMock()
        self.task._request_list.dequeue.return_value = [AsyncMock(), AsyncMock()]

        # ACT
        self.task._start_requests()

        # ASSERT
        self.assertEqual(len(self.task._running_requests), 2)

    def test_check_responses(self):
        task1 = MagicMock(done=MagicMock(return_value=True), exception=MagicMock(return_value=None), result=MagicMock())
        task2 = MagicMock(done=MagicMock(return_value=True), exception=MagicMock(return_value=None), result=MagicMock())
        task3 = MagicMock(done=MagicMock(return_value=False))
        self.task._running_requests = [task1, task2, task3]
        self.task._response_list.put = MagicMock()

        self.task._check_responses()

        self.assertEqual(len(self.task._running_requests), 1)
        self.task._response_list.put.assert_called_once()
