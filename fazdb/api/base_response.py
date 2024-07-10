from abc import ABC
from datetime import datetime


class BaseResponse[B, H](ABC):
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
