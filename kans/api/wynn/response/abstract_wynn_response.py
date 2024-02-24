from abc import ABC
from datetime import datetime as dt
from datetime import timedelta as td
from typing import TypeVar

from ..model import Headers
from kans.util import ResponseSet

T = TypeVar("T")


class AbstractWynnResponse(ResponseSet[T, Headers], ABC):

    def get_expiry_datetime(self) -> dt:
        return self.headers.get_expiry_datetime()

    def get_expiry_timedelta(self) -> td:
        return self.headers.get_expiry_timediff()

    def get_datetime(self) -> dt:
        """
        Get the timestamp of the response.

        Returns:
            dt: The timestamp of the response.
        """
        return self.headers.get_datetime()

    def __repr__(self) -> str:
        return self.__class__.__name__
