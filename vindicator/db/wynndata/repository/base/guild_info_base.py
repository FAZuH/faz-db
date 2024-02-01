from typing import Protocol

from vindicator import GuildInfo, GuildInfoId, Table


class GuildInfoBase(Table[GuildInfo, GuildInfoId], Protocol):
    ...
