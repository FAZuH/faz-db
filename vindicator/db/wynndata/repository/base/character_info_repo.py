from typing import Protocol

from vindicator import CharacterInfo, CharacterInfoId, TableProtocol


class CharacterInfoRepo(TableProtocol[CharacterInfo, CharacterInfoId], Protocol):
    ...
