from typing import Generic, TypeVar

from datetime import datetime

B = TypeVar('B')
H = TypeVar('H')


class ResponseSet(Generic[B, H]):
    """Class for storing data from a HTTP response."""

    def __init__(self, body: B, headers: H) -> None:
        self._body: B = body
        self._headers: H = headers
        self._creation_datetime: datetime = datetime.now()

    @property
    def body(self) -> B:
        return self._body

    @property
    def creation_datetime(self) -> datetime:
        return self._creation_datetime

    @property
    def headers(self) -> H:
        return self._headers
