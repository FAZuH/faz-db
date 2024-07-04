from datetime import datetime as dt
from unittest import TestCase

from fazdb.db.fazdb.model import CharacterHistory


class TestCharacterHistory(TestCase):

    def test_compute_unique_id(self) -> None:
        entity = CharacterHistory(
            character_uuid=b'1', level=1, xp=1, wars=1, playtime=1.0,
            mobs_killed=1, chests_found=1, logins=1, deaths=1, discoveries=1,
            hardcore=False, ultimate_ironman=False, ironman=False, craftsman=False,
            hunted=False, alchemism=1.0, armouring=1.0, cooking=1.0, jeweling=1.0,
            scribing=1.0, tailoring=1.0, weaponsmithing=1.0, woodworking=1.0,
            mining=1.0, woodcutting=1.0, farming=1.0, fishing=1.0, dungeon_completions=1,
            quest_completions=1, raid_completions=1, datetime=dt.now(),
        )
        self.assertIsInstance(entity.unique_id, bytes)

