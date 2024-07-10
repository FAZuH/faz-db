from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._http_request import HttpRequest


class BaseEndpoint(ABC):

    def __init__(self, request: HttpRequest, retries: int, retry_on_exc: bool) -> None:
        self._request = request
        self._retries = retries
        self._retry_on_exc = retry_on_exc

    @property
    @abstractmethod
    def path(self) -> str: ...
