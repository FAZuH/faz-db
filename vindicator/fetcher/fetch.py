from abc import ABC, abstractmethod

from vindicator.typehints import *

# T = TypeVar('T', bound=TypedDict)
# V = TypeVar('V', bound=TypedDict)


#interface
class Fetch(ABC):

    @abstractmethod
    def get_request_queue(self) -> Dict[float, Coro[None]]:
        ...

    @abstractmethod
    def dequeue_dbquery(self) -> Dict[float, Coro[None]]:
        ...

    @abstractmethod
    def run(self) -> None:
        ...

    # Private methods
    @abstractmethod
    async def _request_coro(self, arg: str = "") -> None:
        ...

    @abstractmethod
    async def _dbquery_coro(self, arg: str = "") -> None:
        ...

    @abstractmethod
    def _queue_request(self) -> None:
        ...

    @abstractmethod
    def _queue_dbquery(self) -> None:
        ...
