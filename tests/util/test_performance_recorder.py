# pyright: reportPrivateUsage=none
import asyncio
import unittest
from datetime import datetime, timedelta

from wynndb.logger import PerformanceLogger


class TestPerformanceRecorder(unittest.TestCase):
    def setUp(self) -> None:
        self.recorder = PerformanceLogger()

    async def test_bind_async(self) -> None:
        # PREPARE
        async def async_method() -> int:
            await asyncio.sleep(0.1)
            return 42

        # ACT
        wrapped_method = self.recorder.bind_async(async_method, "test_method")

        # ASSERT
        result = await wrapped_method()
        self.assertEqual(result, 42)

    def test_get_average(self) -> None:
        # PREPARE
        testData1 = [
            (datetime(2022, 1, 1), timedelta(seconds=1)),
            (datetime(2022, 1, 2), timedelta(seconds=2)),
        ]
        self.recorder._data["test_name"] = testData1

        # ACT
        average = self.recorder.get_average("test_name")

        # ASSERT
        assert average is not None
        self.assertAlmostEquals(average, 1.5)

    def test_get_recent(self) -> None:
        # PREPARE
        testData1 = [
            ((datetime.now() - timedelta(days=3)), timedelta(seconds=10)),
            (datetime.now(), timedelta(seconds=1)),
            (datetime.now(), timedelta(seconds=1)),
        ]
        self.recorder._data["test_name"] = testData1

        # ACT
        recent = self.recorder.get_recent(timedelta(days=1), "test_name")

        # ASSERT
        # NOTE: Assert that get_recent returns data within the timedelta
        self.assertSetEqual(set(recent), {
            timedelta(seconds=1),
            timedelta(seconds=1),
        })
