from typing import Protocol

from kans import CharacterInfo, CharacterInfoId, TableProtocol


class CharacterInfoRepo(TableProtocol[CharacterInfo, CharacterInfoId], Protocol):
    ...
