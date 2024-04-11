from wynndb.api.wynn.model.enum import CharacterType


class CharacterTypeField:

    def __init__(self, type_: str) -> None:
        self._type: str = type_

    def __str__(self) -> str:
        return self._type

    def get_kind(self) -> CharacterType:
        """Converts character type string to CharacterType enum.
        If the type string is a reskinned type, it will return the original type."""
        upper_type: str = self._type.upper()
        match upper_type:
            case CharacterType.DARKWIZARD.value:
                return CharacterType.MAGE
            case CharacterType.HUNTER.value:
                return CharacterType.ARCHER
            case CharacterType.KNIGHT.value:
                return CharacterType.WARRIOR
            case CharacterType.NINJA.value:
                return CharacterType.ASSASSIN
            case CharacterType.SKYSEER.value:
                return CharacterType.SHAMAN
            case _:
                if upper_type in (CharacterType.__members__):
                    return CharacterType(upper_type)
                raise ValueError(f"Invalid character type: {self._type}")

    def get_kind_str(self) -> str:
        return self.get_kind().value

    @property
    def type(self) -> str:
        return self._type
