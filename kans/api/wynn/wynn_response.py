from datetime import datetime as dt
from datetime import timedelta as td
from typing import TypeVar

from src import Headers, ResponseSet

T = TypeVar("T")


class WynnResponse(ResponseSet[T, Headers]):

    def get_expiry_datetime(self) -> dt:
        return self.headers.get_expiry_datetime()

    def get_expiry_timediff(self) -> td:
        return self.headers.get_expiry_timediff()

    def get_datetime(self) -> dt:
        """
        Get the timestamp of the response.

        Returns:
            dt: The timestamp of the response.
        """
        return self.headers.get_datetime()
