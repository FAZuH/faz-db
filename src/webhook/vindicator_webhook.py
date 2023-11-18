from datetime import datetime
from typing import TYPE_CHECKING, Callable, Dict, Literal

import aiohttp
import discord
from discord import Webhook
from loguru import logger

from constants import Webhooks

if TYPE_CHECKING:
    from discord import Colour


class VindicatorWebhook:

    MATCH_WEBHOOK_TYPE: Dict[str, str] = {
        "fetch_guild": Webhooks.FETCH_GUILD_WEBHOOK,
        "fetch_online": Webhooks.FETCH_ONLINE_WEBHOOK,
        "fetch_player": Webhooks.FETCH_PLAYER_WEBHOOK,
        "database": Webhooks.DATABASE_WEBHOOK,
        "error": Webhooks.ERROR_WEBHOOK
    }
    MATCH_MESSAGE_TYPE: Dict[str, "Colour"] = {
        "success": discord.Colour.green(),
        "error": discord.Colour.red(),
        "info": discord.Colour.yellow(),
        "connection": discord.Colour.dark_purple(),
        "discord": discord.Colour.blue(),
    }
    MATCH_LOGGER_TYPE: Dict[str, Callable] = {
        "success": logger.success,
        "error": logger.error,
        "info": logger.info,
        "connection": logger.info,
        "discord": logger.info,
    }

    @staticmethod
    async def send(
        webhook_type: Literal["fetch_guild", "fetch_online", "fetch_player", "database", "error"],
        message_type: Literal["success", "error", "info", "connection", "discord"],
        message: str,
        /
    ) -> None:
        url: str = VindicatorWebhook.MATCH_WEBHOOK_TYPE[webhook_type]
        embed_content = discord.Embed(
            title=f"Vindicator/{webhook_type}/{message_type}",
            description=message,
            colour=VindicatorWebhook.MATCH_MESSAGE_TYPE[message_type],
        )
        embed_content.add_field(name="time", value=f"<t:{int(datetime.now().timestamp())}:R>")

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, session=session)
            await webhook.send(embed=embed_content)
        VindicatorWebhook.MATCH_LOGGER_TYPE[message_type](webhook_type + ": " + message.replace('\n', ' ').replace("**", ''))
        return
