from .database_base import DatabaseBase


class VindicatorDatabase(DatabaseBase):

    def __init__(self) -> None:
        return

    @classmethod
    def user(cls) -> str:
        return "root"

    @classmethod
    def password(cls) -> str:
        return "root"

    @classmethod
    def database(cls) -> str:
        return "player_data"
