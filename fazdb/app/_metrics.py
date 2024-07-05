from asyncio import iscoroutine
from functools import wraps
from typing import Any, Callable

from loguru import logger
from prometheus_client import Counter, Summary, start_http_server


class Metrics:
    
    def start(self) -> None:
        start_http_server(8000)
        logger.info("Started prometheus metrics on port 8000")

    def register_summary(self, method: Callable[..., Any], name: str, description: str) -> None:
        summary_metric = Summary(name, description)

        @wraps(method)
        @summary_metric.time()
        async def __async_wrapped(*args, **kwargs):
            return await method(*args, **kwargs)

        @wraps(method)
        @summary_metric.time()
        def __sync_wrapped(*args, **kwargs):
            return method(*args, **kwargs)

        if iscoroutine(method):
            wrapped = __async_wrapped
        else:
            wrapped = __sync_wrapped

        self.__replace(method, wrapped)

    def register_counter(self, method: Callable[..., Any], name: str, description: str) -> None:
        counter_metric = Counter(name, description)

        @wraps(method)
        async def __async_wrapped(*args, **kwargs):
            ret = await method(*args, **kwargs)
            counter_metric.inc()
            return ret

        @wraps(method)
        def __sync_wrapped(*args, **kwargs):
            ret = method(*args, **kwargs)
            counter_metric.inc()
            return ret

        if iscoroutine(method):
            wrapped = __async_wrapped
        else:
            wrapped = __sync_wrapped

        self.__replace(method, wrapped)

    @staticmethod
    def __replace(old_method: Callable[..., Any], new_method: Callable[..., Any]) -> None:
        setattr(new_method, "__self__", old_method.__self__)  # type: ignore
        setattr(old_method.__self__, old_method.__name__, new_method)  # type: ignore
