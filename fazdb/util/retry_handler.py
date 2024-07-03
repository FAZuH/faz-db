from asyncio import iscoroutinefunction
from functools import wraps
from typing import Any, Awaitable, Callable, Iterable

from fazdb.logger.console_logger import ConsoleLogger


class RetryHandler:

    @staticmethod
    def decorator[T, **P](
        max_retries: int,
        exceptions: type[BaseException] | tuple[type[BaseException]]
    ) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
        """ Retries the wrapped function/method `max_retries` times if the exceptions listed in `exceptions` are thrown """
        def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
            @wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                for _ in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions:
                        ConsoleLogger.exception(
                            f"{func.__qualname__} failed. Retrying..."
                            f"args:{str(args)[:30]}\n"
                            f"kwargs:{str(kwargs)[:30]}"
                        )
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def async_decorator[T, **P](
        max_retries: int,
        exceptions: type[BaseException] | tuple[type[BaseException]]
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """ Retries the wrapped function/method `max_retries` times if the exceptions listed in `exceptions` are thrown """
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                for _ in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except exceptions:
                        ConsoleLogger.exception(
                            f"{func.__qualname__} failed. Retrying..."
                            f"args:{str(args)[:30]}\n"
                            f"kwargs:{str(kwargs)[:30]}"
                        )
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def register(
            func: Callable[..., Any | Awaitable[Any]] | Iterable[Callable[..., Any | Awaitable[Any]]],
            max_retries: int,
            exceptions: type[BaseException] | tuple[type[BaseException]]
        ) -> None:
        """ Register object method(s) to be wrapped with an error handler """
        if isinstance(func, Iterable):
            for f in func:
                RetryHandler.register(f, max_retries, exceptions)
            return

        if iscoroutinefunction(func):
            wrapper = RetryHandler.async_decorator(max_retries, exceptions)
        else:
            wrapper = RetryHandler.decorator(max_retries, exceptions)

        wrapped_func = wrapper(func)
        setattr(func.__class__, func.__name__, wrapped_func)