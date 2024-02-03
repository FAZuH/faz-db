from typing import Protocol

from kans import GuildInfo, GuildInfoId, TableProtocol


class GuildInfoRepo(TableProtocol[GuildInfo, GuildInfoId], Protocol):
    ...
