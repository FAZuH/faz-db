class GamemodeColumn:

    def __init__(self, gamemode: list[str] | bytes) -> None:
        self._gamemode = gamemode if isinstance(gamemode, bytes) else self.from_list(gamemode)

    def __str__(self) -> str:
        return self._gamemode.decode("utf-8")

    @classmethod
    def from_list(cls, gamemodes: list[str]) -> bytes:
        bit_position: int
        gm_byte: int = 0  # Initialize a byte to 0
        # Set the corresponding bits in the byte
        for gm in gamemodes:
            match gm:
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
                    raise ValueError(f"Invalid gamemode: {gm}")
            gm_byte |= (1 << bit_position)
        return gm_byte.to_bytes(1, byteorder="big")

    def parse(self) -> list[str]:
        ret = []
        byte_value = int.from_bytes(self.gamemode, byteorder="big")  # Byte to int
        if (byte_value & (1 << 0)) != 0:
            ret.append("hardcore")
        if (byte_value & (1 << 1)) != 0:
            ret.append("ultimate_ironman")
        if (byte_value & (1 << 2)) != 0:
            ret.append("ironman")
        if (byte_value & (1 << 3)) != 0:
            ret.append("craftsman")
        if (byte_value & (1 << 4)) != 0:
            ret.append("hunted")
        return ret

    @property
    def gamemode(self) -> bytes:
        return self._gamemode
