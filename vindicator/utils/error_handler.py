from typing import Any, Awaitable, Callable, Iterable, Set, Type, Union

from loguru import logger


class ErrorHandler:

    _locks: Set[str] = set()

    @classmethod
    def retry(cls, times: int, exceptions: Union[Type[BaseException], Iterable[Type[BaseException]]]) -> Any:
        """ Retries the wrapped function/method `times` times if the exceptions listed in `exceptions` are thrown """
        def decorator(f: Callable):
            def wrapper(*args, **kwargs):
                attempt: int = 1
                while True:
                    try:
                        return f(*args, **kwargs)
                    except exceptions:
                        attempt += 1
                        logger.warning(f"\n{f.__name__} failed. Retrying ({attempt}/{times})...\nargs:{args}\nkwargs:{kwargs}\n")
                        if attempt >= times:
                            logger.error(f"\n{f.__name__} failed. Raising exception to main thread...\nargs:{args}\nkwargs:{kwargs}\n")
                            raise
            return wrapper
        return decorator

    @classmethod
    def aretry(cls, times: int, exceptions: Union[Type[BaseException], Iterable[Type[BaseException]]]) -> Any:
        """ Retries the wrapped function/method `times` times if the exceptions listed in `exceptions` are thrown """
        def decorator(f: Callable):
            async def wrapper(*args, **kwargs):
                attempt: int = 1
                while True:
                    try:
                        return await f(*args, **kwargs)
                    except exceptions:
                        attempt += 1
                        logger.warning(f"\n{f.__name__} failed. Retrying ({attempt}/{times})...\nargs:{args}\nkwargs:{kwargs}\n")
                        if attempt >= times:
                            logger.error(f"\n{f.__name__} failed. Raising exception to main thread...\nargs:{args}\nkwargs:{kwargs}\n")
                            raise
            return wrapper
        return decorator

    @classmethod
    def lock(cls, lock_name: str) -> Any:
        """ Locks the wrapped function/method until the lock is released """
        def decorator(f: Callable):
            def wrapper(*args, **kwargs):
                while getattr(f, lock_name, False):
                    pass
                setattr(f, lock_name, True)
                try:
                    return f(*args, **kwargs)
                finally:
                    setattr(f, lock_name, False)
            return wrapper
        return decorator

    @classmethod
    def alock(cls, lock_name: str):
        """ Locks the wrapped async function/method until the lock is released """
        def decorator(f: Callable[..., Awaitable[Any]]):
            async def wrapper(*args, **kwargs):
                while lock_name in cls._locks:
                    pass
                cls._locks.add(lock_name)
                try:
                    return await f(*args, **kwargs)
                finally:
                    cls._locks.remove(lock_name)
            return wrapper
        return decorator