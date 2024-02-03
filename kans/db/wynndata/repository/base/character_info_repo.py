from typing import Protocol

from src import CharacterInfo, CharacterInfoId, TableProtocol


class CharacterInfoRepo(TableProtocol[CharacterInfo, CharacterInfoId], Protocol):
    ...
