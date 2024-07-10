from datetime import datetime

from dateutil import parser

from ._date_field import DateField


class BodyDateField(DateField):

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, "")

    def to_datetime(self) -> datetime:
        return parser.parse(self.datestr)
