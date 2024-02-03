class CharacterTypeField:

    def __init__(self, type_: str) -> None:
        self._type: str = type_

    def __str__(self) -> str:
        return self._type

    def get_kind(self) -> str:
        upper_type: str = self._type.upper()
        match upper_type:
            case "DARKWIZARD":
                return "MAGE"
            case "HUNTER":
                return "ARCHER"
            case "KNIGHT":
                return "WARRIOR"
            case "NINJA":
                return "ASSASSIN"
            case "SKYSEER":
                return "SHAMAN"
            case _:
                if upper_type in ("MAGE", "ARCHER", "WARRIOR", "ASSASSIN", "SHAMAN"):
                    return upper_type
                raise ValueError(f"Invalid character type: {self._type}")

    @property
    def type(self) -> str:
        return self._type
