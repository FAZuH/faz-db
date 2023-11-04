from typing import Literal

import aiohttp
import discord
from discord import Webhook

from settings import FETCH_GUILD_WEBHOOK, FETCH_PLAYER_WEBHOOK, FETCH_ONLINE_WEBHOOK


class VindicatorWebhook:

    MATCH_WEBHOOK_TYPE = {
        "fetch_guild": FETCH_GUILD_WEBHOOK,
        "fetch_player": FETCH_PLAYER_WEBHOOK,
        "fetch_online": FETCH_ONLINE_WEBHOOK,
    }
    MATCH_MESSAGE_TYPE = {
        "success": discord.Colour.green(),
        "error": discord.Colour.red(),
        "info": discord.Colour.yellow(),
        "connection": discord.Colour.dark_purple(),
        "discord": discord.Colour.blue(),
    }

    @staticmethod
    async def send(
        webhook_type: Literal["fetch_guild", "fetch_player", "fetch_online", "misc"],
        message_type: Literal["success", "error", "info", "connection", "discord"],
        message: str,
        /
    ) -> None:
        url: str = VindicatorWebhook.MATCH_WEBHOOK_TYPE[webhook_type]
        embed_content = discord.Embed(
            title="Vindicator/" + message_type.upper(),
            description=message,
            colour=VindicatorWebhook.MATCH_MESSAGE_TYPE[message_type],
        )

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, session=session)
            await webhook.send(embed=embed_content)

        return
