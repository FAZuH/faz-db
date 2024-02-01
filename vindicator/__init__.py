# type: ignore
from .constants import __version__
from .constants import *
from .errors import *

# No dependencies
from .api.wynn.model.field.nullable import Nullable
from .api.wynn.model.field.character_type_field import CharacterTypeField
from .api.wynn.model.field.date_field import DateField
from .api.wynn.model.field.gamemode_field import GamemodeField
from .api.wynn.model.field.username_or_uuid_field import UsernameOrUuidField
from .api.wynn.model.field.uuid_field import UuidField
from .db.wynndata.model.gamemode_column import GamemodeColumn
from .db.wynndata.model.uuid_column import UuidColumn
from .db.wynndata.repository.repository import Table
from .tasks.fetch import Fetch
from .tasks.request_level import RequestLevel
from .utils.error_handler import ErrorHandler
# from .utils.logger import Logger
from .utils.ratelimit import Ratelimit
from .api.wynn.response_set import ResponseSet
from .webhook.vindicator_webhook import VindicatorWebhook

# Has Dependencies
from .api.wynn.model.field.body_date_field import BodyDateField  # DateField
from .api.wynn.model.field.header_date_field import HeaderDateField  # DateField
from .api.wynn.model.common.headers import Headers  # HeaderDateField
from .api.wynn.model.guild import Guild  # BodyDateField, UsernameOrUuidField, UuidField
from .api.wynn.model.players import Players  # UsernameOrUuidField
from .api.wynn.model.player import Player  # BodyDateField, CharacterTypeField, GamemodeField, UuidField
from .api.wynn.wynn_response import WynnResponse  # Headers, ResponseSet
from .api.wynn.guild_response import GuildResponse  # Guild, WynnResponse
from .api.wynn.players_response import PlayersResponse  # Players, WynnResponse
from .api.wynn.player_response import PlayerResponse  # Player, WynnResponse
from .db.database_query import DatabaseQuery  # ErrorHandler
from .utils.http_request import HttpRequest  # ResponseSet
from .api.wynn.wynn_api import WynnApi  # HttpRequest, Ratelimit, WynnResponse

# db models.id
from .db.wynndata.model.character_history.character_history_id import CharacterHistoryId
from .db.wynndata.model.character_info.character_info_id import CharacterInfoId
from .db.wynndata.model.guild_history.guild_history_id import GuildHistoryId
from .db.wynndata.model.guild_info.guild_info_id import GuildInfoId
from .db.wynndata.model.guild_member_history.guild_member_history_id import GuildMemberHistoryId
from .db.wynndata.model.online_players.online_players_id import OnlinePlayersId
from .db.wynndata.model.player_activity_history.player_activity_history_id import PlayerActivityHistoryId
from .db.wynndata.model.player_history.player_history_id import PlayerHistoryId
from .db.wynndata.model.player_info.player_info_id import PlayerInfoId

# db models. needs models.id
from .db.wynndata.model.character_history.character_history import CharacterHistory
from .db.wynndata.model.character_info.character_info import CharacterInfo
from .db.wynndata.model.guild_info.guild_info import GuildInfo
from .db.wynndata.model.guild_history.guild_history import GuildHistory
from .db.wynndata.model.guild_member_history.guild_member_history import GuildMemberHistory
from .db.wynndata.model.online_players.online_players import OnlinePlayers
from .db.wynndata.model.player_activity_history.player_activity_history import PlayerActivityHistory
from .db.wynndata.model.player_history.player_history import PlayerHistory
from .db.wynndata.model.player_info.player_info import PlayerInfo

# db base. needs db models
from .db.wynndata.repository.base.character_history_base import CharacterHistoryBase
from .db.wynndata.repository.base.character_info_base import CharacterInfoBase
from .db.wynndata.repository.base.guild_history_base import GuildHistoryBase
from .db.wynndata.repository.base.guild_info_base import GuildInfoBase
from .db.wynndata.repository.base.guild_member_history_base import GuildMemberHistoryBase
from .db.wynndata.repository.base.online_players_base import OnlinePlayersBase
from .db.wynndata.repository.base.player_activity_history_base import PlayerActivityHistoryBase
from .db.wynndata.repository.base.player_history_base import PlayerHistoryBase
from .db.wynndata.repository.base.player_info_base import PlayerInfoBase

# db tables. needs db base
from .db.wynndata.repository.table.guild_history_table import GuildHistoryTable
from .db.wynndata.repository.table.guild_info_table import GuildInfoTable
from .db.wynndata.repository.table.guild_member_history_table import GuildMemberHistoryTable
from .db.wynndata.repository.table.character_history_table import CharacterHistoryTable
from .db.wynndata.repository.table.character_info_table import CharacterInfoTable
from .db.wynndata.repository.table.online_players_table import OnlinePlayersTable
from .db.wynndata.repository.table.player_activity_history_table import PlayerActivityHistoryTable
from .db.wynndata.repository.table.player_history_table import PlayerHistoryTable
from .db.wynndata.repository.table.player_info_table import PlayerInfoTable

# needs all tables above
from .db.wynndata.wynndata_repository import WynnDataRepository

# tasks. needs all above
from .tasks.fetch_queue import FetchQueue  # Request
from .tasks.request import Request  # ResponseSet
from .tasks.guild_request import GuildRequest  # Request, RequestLevel, WynnRequest, GuildStats
from .tasks.online_request import OnlineRequest  # Request, RequestLevel, WynnRequest, Players
from .tasks.player_request import PlayerRequest  # Request, RequestLevel, WynnRequest, PlayerStats
from .tasks.fetch_online import FetchOnline # Fetch, Players, OnlineRequest, PlayerRequest
from .tasks.fetch_player import FetchPlayer  # Fetch, FetchBase, FetchOnline, PlayerStats
from .tasks.fetch_guild import FetchGuild  # Fetch, FetchBase, FetchPlayer, GuildStats
from .tasks.fetch_core import FetchCore  # Fetch, FetchGuild, FetchOnline, FetchPlayer, RequestLevel, WynnApi
