from typing import Protocol

from vindicator import CharacterInfo, CharacterInfoId, Table


class CharacterInfoRepo(Table[CharacterInfo, CharacterInfoId], Protocol):
    ...
