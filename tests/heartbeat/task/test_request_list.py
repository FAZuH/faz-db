# pyright: reportPrivateUsage=none
import unittest
from datetime import datetime as dt

from kans.heartbeat.task import RequestList


class TestRequestList(unittest.TestCase):

    def setUp(self) -> None:
        self.request_list = RequestList()

    async def mock_coro(self, arg: str) -> str:
        return arg

    def test_enqueue_and_dequeue(self) -> None:
        # sourcery skip: class-extract-method
        # PREPARE
        testCoro1 = self.mock_coro('foo')
        testRequestTs1 = dt.now().timestamp() - 100

        # ACT
        self.request_list.enqueue(testRequestTs1, testCoro1)

        # ASSERT
        # NOTE: Assert that the request is enqueued properly
        self.assertEqual(len(self.request_list._list), 1)
        self.assertEqual(self.request_list._list[0].coro, testCoro1)
        self.assertEqual(self.request_list._list[0]._req_ts, testRequestTs1)

        # ACT
        result = self.request_list.dequeue(1)

        # ASSERT
        # NOTE: Assert that the correct request is dequeued
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], testCoro1)

    def test_dequeue_with_request_ts(self) -> None:
        # PREPARE
        testCoro1 = self.mock_coro('foo')
        testCoro2 = self.mock_coro('bar')
        testRequestTs1 = dt.now().timestamp() - 100
        testRequestTs2 = dt.now().timestamp() - 200  # earlier timestamp

        self.request_list.enqueue(testRequestTs1, testCoro1)
        self.request_list.enqueue(testRequestTs2, testCoro2)

        # ACT
        result = self.request_list.dequeue(1)

        # ASSERT
        # NOTE: Assert that the request with the earliest timestamp is dequeued first
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], testCoro2)
        remaining_item = self.request_list._list.pop()
        # NOTE: Assert that the remaining item is the one with the later timestamp
        self.assertEqual(remaining_item.coro, testCoro1)
        self.assertEqual(remaining_item._req_ts, testRequestTs1)

    def test_dequeue_with_priority(self) -> None:
        # PREPARE
        testCoro1 = self.mock_coro('foo')
        testCoro2 = self.mock_coro('bar')
        testRequestTs1 = dt.now().timestamp() - 100
        testRequestTs2 = dt.now().timestamp() - 50  # should still return higher priority
        self.request_list.enqueue(testRequestTs1, testCoro1, priority=100)
        self.request_list.enqueue(testRequestTs2, testCoro2, priority=200)  # higher priority

        # ACT
        result = self.request_list.dequeue(1)

        # ASSERT
        self.assertEqual(len(result), 1)
        self.assertEqual(result.pop(), testCoro2)

    def test_iter(self) -> None:
        # PREPARE
        coro1 = self.mock_coro("foo")
        coro2 = self.mock_coro("bar")
        request_ts = dt.now().timestamp()
        self.request_list.enqueue(request_ts, coro1)
        self.request_list.enqueue(request_ts, coro2)

        # ACT
        result = list(self.request_list.iter())

        # ASSERT
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].coro, coro1)
        self.assertEqual(result[1].coro, coro2)

    def test_request_item_is_eligible(self) -> None:
        # PREPARE
        testCoro1 = self.mock_coro("foo")
        testRequestTs1 = dt.now().timestamp() - 1 # Past timestamp
        request_item = RequestList.RequestItem(testCoro1, 100, testRequestTs1)

        # ASSERT
        self.assertTrue(request_item.is_eligible())

    def test_request_item_is_not_eligible(self) -> None:
        # PREPARE
        testCoro1 = self.mock_coro("foo")
        testRequestTs1 = dt.now().timestamp() + 1000  # Future timestamp
        request_item = RequestList.RequestItem(testCoro1, 100, testRequestTs1)

        # ASSERT
        # NOTE: Assert that request item is not eligible
        self.assertFalse(request_item.is_eligible())

    def test_request_item_comparison(self) -> None:
        # PREPARE
        testCoro1 = self.mock_coro("foo")
        testCoro2 = self.mock_coro("bar")
        request_item1 = RequestList.RequestItem(testCoro1, 100, 0)
        request_item2 = RequestList.RequestItem(testCoro2, 200, 0)

        # ASSERT
        self.assertLess(request_item2, request_item1)

    def test_request_item_equality(self) -> None:
        # PREPARE
        testCoro1 = self.mock_coro("foo")
        testCoro2 = self.mock_coro("foo")
        request_ts = dt.now().timestamp()
        request_item1 = RequestList.RequestItem(testCoro1, 100, request_ts)
        request_item2 = RequestList.RequestItem(testCoro2, 100, request_ts)

        # ASSERT
        self.assertEqual(request_item1, request_item2)

    def tearDown(self) -> None:
        pass
