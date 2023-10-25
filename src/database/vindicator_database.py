from .database_base import DatabaseBase


class VindicatorDatabase(DatabaseBase):
    _database = "player_data"

    @classmethod
    async def ainit(cls):
        await VindicatorDatabase._ainit(cls)
