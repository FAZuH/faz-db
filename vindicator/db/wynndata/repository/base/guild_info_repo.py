from typing import Protocol

from vindicator import GuildInfo, GuildInfoId, Table


class GuildInfoRepo(Table[GuildInfo, GuildInfoId], Protocol):
    ...
