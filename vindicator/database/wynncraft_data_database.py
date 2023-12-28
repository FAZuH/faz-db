from vindicator import DatabaseBase


class WynncraftDataDatabase(DatabaseBase):

    def __init__(self) -> None:
        return

    @classmethod
    def database(cls) -> str:
        return "wynncraft_data"

    @classmethod
    def password(cls) -> str:
        return "root"

    @classmethod
    def retries(cls) -> int:
        return 3

    @classmethod
    def user(cls) -> str:
        return "root"
