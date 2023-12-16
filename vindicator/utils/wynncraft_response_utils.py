from datetime import datetime
import hashlib
from dateutil.tz import tzutc
from typing import List


class WynncraftResponseUtils:

    @staticmethod
    def fix_chartype(char_type: str) -> str:
        char_type = char_type.upper()
        CHARTYPE_MATCH = {
            "DARKWIZARD" : "MAGE",
            "HUNTER": "ARCHER",
            "KNIGHT": "WARRIOR",
            "NINJA": "ASSASSIN",
            "SKYSEER": "SHAMAN"
        }
        return CHARTYPE_MATCH[char_type] if char_type in CHARTYPE_MATCH else char_type

    @staticmethod
    def parse_datestr1(datestr: str) -> float:
        return datetime.strptime(datestr, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tzutc()).timestamp()

    @staticmethod
    def parse_datestr2(datestr: str) -> float:
        return datetime.fromisoformat(datestr).timestamp()

    @staticmethod
    def parse_uuid(uuidbytes: bytes) -> str:
        return uuidbytes.hex().upper()

    @staticmethod
    def format_uuid(uuidstr: str) -> bytes:
        return bytes.fromhex(uuidstr.replace("-", ""))

    @staticmethod
    def parse_gamemode(gamemodebyte: bytes) -> List[str]:
        ret = []

        byte_value = int.from_bytes(gamemodebyte, byteorder='big')  # Byte to int
        is_hardcore = (byte_value & (1 << 0)) != 0
        is_ultimate = (byte_value & (1 << 1)) != 0
        is_ironman = (byte_value & (1 << 2)) != 0
        is_craftsman = (byte_value & (1 << 3)) != 0
        is_hunted = (byte_value & (1 << 4)) != 0

        if is_hardcore:
            ret.append("hardcore")
        if is_ultimate:
            ret.append("ultimate_ironman")
        if is_ironman:
            ret.append("ironman")
        if is_craftsman:
            ret.append("craftsman")
        if is_hunted:
            ret.append("hunted")

        return ret

    @staticmethod
    def format_gamemodes(gamemodeslist: List[str]) -> bytes:
        gamemode_byte = 0  # Initialize a byte to 0

        gamemode_mapping = {
            "hardcore": 0,
            "ultimate_ironman": 1,
            "ironman": 2,
            "craftsman": 3,
            "hunted": 4
        }

        # Set the corresponding bits in the byte
        for gamemode in gamemodeslist:
            if gamemode not in gamemode_mapping:
                raise ValueError(f"Invalid gamemode: {gamemode}")

            bit_position = gamemode_mapping[gamemode]
            gamemode_byte |= (1 << bit_position)

        return gamemode_byte.to_bytes(1, byteorder='big')

    @staticmethod
    def compute_hash(string: str) -> bytes:
        return hashlib.sha256(string.encode()).digest()
