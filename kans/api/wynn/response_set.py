from typing import Generic, TypeVar

from datetime import datetime as dt

B = TypeVar('B')
H = TypeVar('H')


class ResponseSet(Generic[B, H]):
    """Base class for storing importation from a HTTP response."""

    def __init__(self, body: B, headers: H) -> None:
        self._body: B = body
        self._headers: H = headers
        self._creation_datetime: dt = dt.now()

    @property
    def body(self) -> B:
        return self._body

    @property
    def creation_datetime(self) -> dt:
        return self._creation_datetime

    @property
    def headers(self) -> H:
        return self._headers
