from dataclasses import asdict
from time import perf_counter
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from discord.ext import tasks

from .fetch_base import FetchBase
from bot_logger import log_stalk
from modules.database.constants import StalkerDatabaseTable
from modules.database.objects import GuildMember, PlayerGeneral, TaskTimestamp
from modules.database.stalker_databases import GuildMemberDatabase
from modules.error_handler import ErrorHandler
from modules.stalker.constants import StalkFetch
from modules.utils import PaintLog

if TYPE_CHECKING:
    from cogs.stalker import Stalker
    from corkus.objects.guild import Guild


class FetchGuild:
    def __init__(self, pcls: 'Stalker'):
        self.pcls: Stalker = pcls
        self.fetched_guilds: List['Guild'] = []
        self.guild_members: List[Dict[str, Any]] = []
        self.guilds: List[Dict[str, Any]] = []

    @tasks.loop(seconds=StalkFetch.FETCH_GUILD_PERIOD)
    async def run(self):
        t0 = perf_counter()
        self.fetched_guilds = []
        self.guild_members = []
        self.guilds = []

        try:
            await self.fetch_guilds()
            self.convert_guild_objs()
            await self.to_db_guild_member()

        except Exception as e:
            await ErrorHandler.handle_loop_exc(self, e)

        log_stalk.info(f'{PaintLog.self(self, "success")} {perf_counter()-t0:.1f}s')

    async def fetch_guilds(self):
        fetched_guild_names: List[str] = []
        online_pg = await PlayerGeneral.get_online()

        for pg in online_pg:
            if not pg.guild_name or pg.guild_name in fetched_guild_names:
                continue

            guild = await FetchBase.get_guild_stats(pg.guild_name)
            if not guild:
                continue

            fetched_guild_names.append(guild.name)
            self.fetched_guilds.append(guild)

        await TaskTimestamp.update_db('fetch_guild')

    def convert_guild_objs(self):
        for guild in self.fetched_guilds:
            # self.guilds.append(asdict(Guild.from_guild(guild)))
            for member in guild.members:
                try:
                    self.guild_members.append(asdict(GuildMember.from_member(guild, member)))

                except Exception:
                    continue

    async def to_db_guild_member(self):
        query = (
            f"INSERT OR REPLACE INTO {StalkerDatabaseTable.GUILD_MEMBER} "
            "(username, uuid, rank, contributed_xp, join_date, guild_name, timestamp) VALUES "
            "(:username, :uuid, :rank, :contributed_xp, :join_date, :guild_name, :timestamp)"
        )
        await GuildMemberDatabase.writemany(query, self.guild_members)
