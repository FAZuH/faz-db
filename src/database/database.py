from settings import 
from .database_base import DatabaseBase


class GuildMemberDatabase(DatabaseBase):
    _directory = DatabaseDirectory.GUILD_MEMBER_DIR

    @classmethod
    async def ainit(cls):
        await cls._init_class_attrs(cls)


class PlayerActivityDatabase(DatabaseBase):
    _directory = DatabaseDirectory.PLAYER_ACTIVITY_DIR

    @classmethod
    async def ainit(cls):
        await cls._init_class_attrs(cls)


class PlayerCharacterDatabase(DatabaseBase):
    _directory = DatabaseDirectory.PLAYER_CHARACTER_DIR

    @classmethod
    async def ainit(cls):
        await cls._init_class_attrs(cls)


class PlayerGeneralDatabase(DatabaseBase):
    _directory = DatabaseDirectory.PLAYER_GENERAL_DIR

    @classmethod
    async def ainit(cls):
        await cls._init_class_attrs(cls)


class PlayerStatisticsDatabase(DatabaseBase):
    _directory = DatabaseDirectory.PLAYER_STATISTICS_DIR

    @classmethod
    async def ainit(cls):
        await cls._init_class_attrs(cls)


class StalkerConfigDatabase(DatabaseBase):
    _directory = DatabaseDirectory.STALKER_CONFIG_DIR

    @classmethod
    async def ainit(cls):
        await cls._init_class_attrs(cls)
