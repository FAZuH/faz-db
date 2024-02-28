import unittest
from datetime import datetime as dt
from typing import Coroutine
from unittest.mock import MagicMock

from kans.heartbeat.task.request_list import RequestList


class TestRequestList(unittest.TestCase):

    def setUp(self) -> None:
        self.request_list = RequestList()

    async def mock_coro(self, arg: str) -> str:
        return arg

    def test_put_and_get(self) -> None:
        coro = self.mock_coro('foo')
        request_ts = dt.now().timestamp() - 100
        self.request_list.enqueue(request_ts, coro)

        result = self.request_list.get(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], coro)

    def test_put_with_priority(self) -> None:
        coro1 = self.mock_coro('foo')
        coro2 = self.mock_coro('bar')
        request_ts = dt.now().timestamp() - 100

        self.request_list.enqueue(request_ts, coro1, priority=100)
        self.request_list.enqueue(request_ts, coro2, priority=200)  # higher priority

        result = self.request_list.get(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.pop(), coro2)

    def test_get_with_empty_list(self) -> None:
        result = self.request_list.get(1)

        self.assertEqual(len(result), 0)

    def test_iter(self) -> None:
        coro1 = self.mock_coro("foo")
        coro2 = self.mock_coro("bar")
        request_ts = dt.now().timestamp()

        self.request_list.enqueue(request_ts, coro1)
        self.request_list.enqueue(request_ts, coro2)

        result = list(self.request_list.iter())

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].coro, coro1)
        self.assertEqual(result[1].coro, coro2)

    def test_request_item_is_elligible(self) -> None:
        coro = self.mock_coro("foo")
        request_ts = dt.now().timestamp() - 1
        request_item = RequestList.RequestItem(coro, 100, request_ts)

        self.assertTrue(request_item.is_elligible())

    def test_request_item_is_not_elligible(self) -> None:
        coro = MagicMock(spec=Coroutine)
        request_ts = dt.now().timestamp() + 10  # Future timestamp
        request_item = RequestList.RequestItem(coro, 100, request_ts)

        self.assertFalse(request_item.is_elligible())

    def test_request_item_comparison(self) -> None:
        coro1 = self.mock_coro("foo")
        coro2 = self.mock_coro("bar")

        request_item1 = RequestList.RequestItem(coro1, 100, 0)
        request_item2 = RequestList.RequestItem(coro2, 200, 0)

        self.assertLess(request_item2, request_item1)

    def test_request_item_equality(self) -> None:
        coro1 = self.mock_coro("foo")
        coro2 = self.mock_coro("foo")
        request_ts = dt.now().timestamp()

        request_item1 = RequestList.RequestItem(coro1, 100, request_ts)
        request_item2 = RequestList.RequestItem(coro2, 100, request_ts)

        self.assertEqual(request_item1, request_item2)

    def tearDown(self) -> None:
        pass
