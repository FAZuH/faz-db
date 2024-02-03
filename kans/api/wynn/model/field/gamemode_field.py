class GamemodeField:

    def __init__(self, gamemodes: list[str]) -> None:
        self._gamemodes: list[str] = gamemodes

    def to_bytes(self) -> bytes:
        bit_position: int
        gamemode_byte: int = 0  # Initialize a byte to 0
        # Set the corresponding bits in the byte
        for gamemode in self._gamemodes:
            match gamemode:
                case "hardcore":
                    bit_position = 0
                case "ultimate_ironman":
                    bit_position = 1
                case "ironman":
                    bit_position = 2
                case "craftsman":
                    bit_position = 3
                case "hunted":
                    bit_position = 4
                case _:
                    raise ValueError(f"Invalid gamemode: {gamemode}")
            gamemode_byte |= (1 << bit_position)
        return gamemode_byte.to_bytes(1, byteorder="big")

    @property
    def gamemodes(self) -> list[str]:
        return self._gamemodes
