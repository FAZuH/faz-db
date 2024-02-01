class GamemodeColumn:

    def __init__(self, gamemode: bytes) -> None:
        self._gamemode: bytes = gamemode

    def __str__(self) -> str:
        return self._gamemode.decode("utf-8")

    def parse(self) -> list[str]:
        ret = []
        byte_value = int.from_bytes(self.gamemode, byteorder='big')  # Byte to int
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