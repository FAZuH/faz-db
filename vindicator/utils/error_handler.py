from functools import wraps
from inspect import iscoroutinefunction
from typing import Awaitable, Callable, ParamSpec, TypeVar, Iterable

from loguru import logger

T = TypeVar("T")
P = ParamSpec("P")


class ErrorHandler:

    @staticmethod
    def retry_decorator(max_retries: int, exceptions: type[BaseException] | Iterable[type[BaseException]]):
        """ Retries the wrapped function/method `times` times if the exceptions listed in `exceptions` are thrown """
        def decorator(f: Callable[P, T]) -> Callable[P, Awaitable[T]]:
            @wraps(f)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:  # type: ignore
                for _ in range(max_retries + 1):
                    try:
                        return (await f(*args, **kwargs)) if iscoroutinefunction(f) else f(*args, **kwargs)
                    except exceptions:
                        logger.error((
                            f"{f.__qualname__} failed. Raising exception to main thread...\n"
                            f"args:{str(args)[:30]}\n"
                            f"kwargs:{str(kwargs)[:30]}"
                        ))
                        raise
            return wrapper
        return decorator
