from typing import Protocol

from src import GuildInfo, GuildInfoId, TableProtocol


class GuildInfoRepo(TableProtocol[GuildInfo, GuildInfoId], Protocol):
    ...
