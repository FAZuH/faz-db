import asyncio
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar, Iterable

from loguru import logger

T = TypeVar("T")
P = ParamSpec("P")


class ErrorHandler:

    _locks: dict[str, asyncio.Lock] = {}

    @classmethod
    def lock_decorator(cls, lock_name: str):
        """Locks the wrapped async function/method until the lock is released"""
        def decorator(f: Callable[P, T]) -> Callable[P, Coroutine[Any, Any, T]]:
            @wraps(f)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                lock = cls._locks.get(lock_name)
                if not lock:
                    lock = asyncio.Lock()
                    cls._locks[lock_name] = lock
                async with lock:
                    res = (await f(*args, **kwargs)) if iscoroutinefunction(f) else f(*args, **kwargs)
                return res
            return wrapper
        return decorator

    @staticmethod
    def retry_decorator(times: int, exceptions: type[BaseException] | Iterable[type[BaseException]]):
        """ Retries the wrapped function/method `times` times if the exceptions listed in `exceptions` are thrown """
        def decorator(f: Callable[P, T]) -> Callable[P, Coroutine[Any, Any, T]]:
            @wraps(f)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                attempt: int = 0
                while True:
                    try:
                        return (await f(*args, **kwargs)) if iscoroutinefunction(f) else f(*args, **kwargs)  # type: ignore
                    except exceptions:
                        attempt += 1
                        if attempt > times:
                            logger.error(
                                f"""
                                {f.__qualname__} failed. Raising exception to main thread...\n
                                args:{str(args)[:30]}\n
                                kwargs:{str(kwargs)[:30]}
                                """
                            )
                            raise
                        logger.warning(
                            f"""
                            {f.__qualname__} failed. Retrying ({attempt}/{times})...\n
                            args:{str(args)[:30]}\n
                            kwargs:{str(kwargs)[:30]}\n
                            """
                        )
            return wrapper
        return decorator
