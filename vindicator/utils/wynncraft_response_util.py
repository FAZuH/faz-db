from datetime import datetime as dt
from dateutil.tz import tzutc
import hashlib

from vindicator.constants import *
from vindicator.typehints import *


class WynncraftResponseUtil:

    @staticmethod
    def fix_chartype(chartype: str) -> str:
        fixed_chartype = chartype.upper()
        match fixed_chartype:
            case "DARKWIZARD":
                fixed_chartype = "MAGE"
            case "HUNTER":
                fixed_chartype = "ARCHER"
            case "KNIGHT":
                fixed_chartype = "WARRIOR"
            case "NINJA":
                fixed_chartype = "ASSASSIN"
            case "SKYSEER":
                fixed_chartype = "SHAMAN"
        return fixed_chartype

    @staticmethod
    def resp_to_sqldt(datestr: str) -> str:
        """Formats Wynncraft API response date format (`Sat, 16 Dec 2023 15:15:37 GMT`) to MySQL datetime format"""
        return dt.strptime(datestr, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tzutc()).strftime(MYSQL_DT_FMT)

    @staticmethod
    def resp_to_timestamp(datestr: str) -> float:
        """Formats Wynncraft API response date format (`Sat, 16 Dec 2023 15:15:37 GMT`) to UNIX timestamp"""
        return dt.strptime(datestr, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tzutc()).timestamp()

    @staticmethod
    def iso_to_sqldt(datestr: str) -> str:
        """Formats ISO 8601 date format (`2023-12-16T15:15:37Z`) to MySQL datetime format"""
        return dt.fromisoformat(datestr).strftime(MYSQL_DT_FMT)

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
        bit_position: int
        gamemode_byte: int = 0  # Initialize a byte to 0
        # Set the corresponding bits in the byte
        for gamemode in gamemodeslist:
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
        return gamemode_byte.to_bytes(1, byteorder='big')

    @staticmethod
    def compute_hash(string: str) -> bytes:
        return hashlib.sha256(string.encode()).digest()
