from typing_extensions import override
from datetime import datetime as dt

from vindicator import DateField


class BodyDateField(DateField):

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, "")

    @override
    def to_datetime(self) -> dt:
        return dt.fromisoformat(self.datestr)
