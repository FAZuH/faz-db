from typing import Protocol

from vindicator import CharacterHistory, CharacterHistoryId, Table


class CharacterHistoryRepo(Table[CharacterHistory, CharacterHistoryId], Protocol):
    ...
