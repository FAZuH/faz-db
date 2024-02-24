from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kans.util import HttpRequest


class AbstractEndpoint(ABC):
    """<<abstract>>
    An endpoint that can be used to get data from a source."""

    def __init__(self, request: HttpRequest, retries: int, retry_on_exc: bool) -> None:
        self._request = request
        self._retries = retries
        self._retry_on_exc = retry_on_exc
