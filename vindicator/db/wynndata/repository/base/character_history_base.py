from typing import Protocol

from vindicator import CharacterHistory, CharacterHistoryId, Table


class CharacterHistoryBase(Table[CharacterHistory, CharacterHistoryId], Protocol):
    ...
