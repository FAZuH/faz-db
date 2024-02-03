from typing import Protocol

from src import CharacterHistory, CharacterHistoryId, TableProtocol


class CharacterHistoryRepo(TableProtocol[CharacterHistory, CharacterHistoryId], Protocol):
    ...
