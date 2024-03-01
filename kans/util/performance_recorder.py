from datetime import datetime, timedelta
from functools import wraps
from threading import Lock
from time import perf_counter
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeVar

P = ParamSpec('P')
T = TypeVar('T')


class PerformanceRecorder:

    def __init__(self) -> None:
        self._data: dict[str, dict[datetime, timedelta]] = {}
        """{name: {callDatetime: dallDuration}}"""
        self._lock = Lock()

        self._MAX_CACHE = 1_000
        """Max amount of cache for each name. If exceeded, the oldest data will be removed."""

    def listen_async(self, method: Callable[P, Awaitable[T]], name: str) -> Callable[P, Coroutine[Any, Any, T]]:
        """Decorator to record the duration of an async method. The duration will be recorded in `timedelta`."""
        self._data[name] = {}
        @wraps(method)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            t1 = perf_counter()
            res = await method(*args, **kwargs)
            with self._lock:
                self._data[name][datetime.now()] = timedelta(seconds=perf_counter() - t1)
                if len(self._data[name]) > self._MAX_CACHE:
                    # KeyError won't happen here
                    self._data[name].pop(min(self._data[name]))
            return res
        return wrapped

    def get_data(self, name: str) -> dict[datetime, timedelta]:
        with self._lock:
            if name in self._data:
                return self._data[name].copy()
            else:
                return {}

    def get_average(self, name: str) -> float:
        """Get average duration of calls in seconds. If no data, return 0."""
        with self._lock:
            if name in self._data and len(self._data[name]) > 0:
                return sum((e.seconds for e in self._data[name].values())) / len(self._data[name])
            else:
                return 0

    def get_recent(self, timedelta: timedelta, name: str) -> list[timedelta]:
        """Get all calls within `timedelta` from now. If no data, return empty list."""
        with self._lock:
            if name in self._data:
                now = datetime.now()
                return [call_duration for call_dt, call_duration in self._data[name].items() if (now - call_dt) < timedelta]
            else:
                return []
