from datetime import datetime as dt
from dateutil import parser

from kans import DateField


class BodyDateField(DateField):

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, "")

    def to_datetime(self) -> dt:
        return parser.parse(self.datestr)
