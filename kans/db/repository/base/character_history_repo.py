from typing import Protocol

from kans import CharacterHistory, CharacterHistoryId, TableProtocol


class CharacterHistoryRepo(TableProtocol[CharacterHistory, CharacterHistoryId], Protocol):
    ...
