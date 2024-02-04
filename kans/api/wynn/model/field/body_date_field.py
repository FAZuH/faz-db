from datetime import datetime as dt
from dateutil import parser

from typing_extensions import override

from kans import DateField


class BodyDateField(DateField):

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, "")

    @override
    def to_datetime(self) -> dt:
        return parser.parse(self.datestr)
