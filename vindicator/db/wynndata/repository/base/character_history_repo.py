from typing import Protocol

from vindicator import CharacterHistory, CharacterHistoryId, TableProtocol


class CharacterHistoryRepo(TableProtocol[CharacterHistory, CharacterHistoryId], Protocol):
    ...
