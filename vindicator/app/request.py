from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from vindicator import FetchCore, RequestLevel

T = TypeVar('T')


class Request(ABC, Generic[T]):

    def __init__(self, fetch_core: FetchCore, level: RequestLevel, request_arg: str = '') -> None:
        self._fetch_core = fetch_core
        self._level = level
        self._request_arg = request_arg
        self._done = False
        self._response: T

    @abstractmethod
    async def requeue(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def run(self) -> None:
        raise NotImplementedError

    def __lt__(self, other: Request[T]) -> bool:
        """PriorityQueue compares the item with `<` if priority_value already exists.
        This magic method is implemented as a fix for that.
        The goal is to have Player and Guild request to be equal."""
        if self.level >= 2 and other.level >= 2:
            return False
        return self.level < other.level

    @property
    def done(self) -> bool:
        return self._done

    @property
    def level(self) -> RequestLevel:
        return self._level

    @property
    def request_arg(self) -> str:
        return self._request_arg

    @property
    def response(self) -> T:
        return self._response

    @response.setter
    def response(self, item: T) -> None:
        self._response = item
