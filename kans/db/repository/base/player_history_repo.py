from typing import Protocol

from kans import PlayerHistory, PlayerHistoryId, TableProtocol


class PlayerHistoryRepo(TableProtocol[PlayerHistory, PlayerHistoryId], Protocol):
    ...
