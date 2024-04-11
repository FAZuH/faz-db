from ..enum import Gamemode


class GamemodeField:

    def __init__(self, gamemodes: list[str]) -> None:
        self._gamemodes_str: list[str] = gamemodes
        self._gamemodes: list[Gamemode] = []

        for gm in gamemodes:
            match gm.upper():
                case Gamemode.HARDCORE.value:
                    self._gamemodes.append(Gamemode.HARDCORE)
                case Gamemode.ULTIMATE_IRONMAN.value:
                    self._gamemodes.append(Gamemode.ULTIMATE_IRONMAN)
                case Gamemode.IRONMAN.value:
                    self._gamemodes.append(Gamemode.IRONMAN)
                case Gamemode.CRAFTSMAN.value:
                    self._gamemodes.append(Gamemode.CRAFTSMAN)
                case Gamemode.HUNTED.value:
                    self._gamemodes.append(Gamemode.HUNTED)
                case _:
                    raise ValueError(f"Invalid gamemode: {gm}")

    def get_liststr(self) -> list[str]:
        return self._gamemodes_str

    def is_hardcore(self) -> bool:
        return Gamemode.HARDCORE in self._gamemodes

    def is_ultimate_ironman(self) -> bool:
        return Gamemode.ULTIMATE_IRONMAN in self._gamemodes

    def is_ironman(self) -> bool:
        return Gamemode.IRONMAN in self._gamemodes

    def is_craftsman(self) -> bool:
        return Gamemode.CRAFTSMAN in self._gamemodes

    def is_hunted(self) -> bool:
        return Gamemode.HUNTED in self._gamemodes

    @property
    def gamemodes(self) -> list[Gamemode]:
        return self._gamemodes
