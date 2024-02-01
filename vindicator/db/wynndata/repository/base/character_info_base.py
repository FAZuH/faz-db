from typing import Protocol

from vindicator import CharacterInfo, CharacterInfoId, Table


class CharacterInfoBase(Table[CharacterInfo, CharacterInfoId], Protocol):
    ...
