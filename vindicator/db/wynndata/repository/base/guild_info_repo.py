from typing import Protocol

from vindicator import GuildInfo, GuildInfoId, TableProtocol


class GuildInfoRepo(TableProtocol[GuildInfo, GuildInfoId], Protocol):
    ...
