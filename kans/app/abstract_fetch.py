from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, Generic, TypeVar

if TYPE_CHECKING:
    from src import FetchCore, WynnDataRepository

T = TypeVar('T')


class AbstractFetch(ABC, Generic[T]):
    """<<abstract>>
    extended by `FetchGuild`, `FetchOnline`, `FetchPlayer`
    """

    def __init__(self, fetch_core: FetchCore) -> None:
        self._fetch_core = fetch_core
        self._request: list[T] = []

    def append_request(self, request: T) -> None:
        self._request.append(request)

    def pop(self) -> T:
        return self._request.pop()

    def _request_pop_iterator(self) -> Generator[T, None, None]:
        """Concurrent-safe get all request."""
        while len(self._request) != 0:
            yield self._request.pop()

    @abstractmethod
    async def run(self) -> None:
        raise NotImplementedError

    @property
    def fetch_core(self) -> FetchCore:
        return self._fetch_core

    @property
    def wynnrepo(self) -> WynnDataRepository:
        return self.fetch_core.wynnrepo
