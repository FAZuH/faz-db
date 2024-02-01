from time import time
from typing import Any, Literal

from aiohttp import ClientSession
from discord import Colour, Embed, Webhook

from vindicator import config


class VindicatorWebhook:

    MATCH_WEBHOOK_TYPE: dict[str, str] = {
        "database": config["DATABASE_WEBHOOK"],
        "error": config["ERROR_WEBHOOK"],
        "fetch_guild": config["FETCH_GUILD_WEBHOOK"],
        "fetch_online": config["FETCH_ONLINE_WEBHOOK"],
        "fetch_player": config["FETCH_PLAYER_WEBHOOK"],
        "wynncraft_request": config["WYNNCRAFT_REQUEST_WEBHOOK"],
    }
    MATCH_MESSAGE_TYPE: dict[str, Colour] = {
        "success": Colour.green(),
        "error": Colour.red(),
        "info": Colour.dark_grey(),
        "request": Colour.dark_purple(),
        "read": Colour.teal(),
        "write": Colour.dark_teal(),
        "update": Colour.dark_green(),
    }

    @staticmethod
    async def send(
        webhook_type: Literal["fetch_guild", "fetch_online", "fetch_player", "database", "error"],
        message_type: Literal["success", "error", "info", "request", "read", "write", "update"],
        message: str
    ) -> None:
        url: str = VindicatorWebhook.MATCH_WEBHOOK_TYPE[webhook_type]
        embed_content = Embed(
            title=message_type,
            description=message,
            colour=VindicatorWebhook.MATCH_MESSAGE_TYPE[message_type],
        )
        embed_content.add_field(name="", value=f"<t:{int(time())}:R>")

        async with ClientSession() as session:
            webhook = Webhook.from_url(url, session=session)
            await webhook.send(embed=embed_content)

    @staticmethod
    async def log(
        webhook_type: Literal["database", "error", "fetch_guild", "fetch_online", "fetch_player", "wynncraft_request"],
        message_type: Literal["success", "error", "info", "request", "read", "write", "update"],
        stats: dict[str, Any],
        title: str = ''
    ) -> None:
        url: str = VindicatorWebhook.MATCH_WEBHOOK_TYPE[webhook_type]
        embed_content = Embed(
            title=message_type,
            colour=VindicatorWebhook.MATCH_MESSAGE_TYPE[message_type],
        )
        embed_content.description = f"**{title}**\n" if title else ''
        embed_content.description += f"<@{config['DEVELOPER_DISCORD_ID']}>\n" if message_type == "error" else ''
        embed_content.description += '\n'.join([f"`{k:15}:`**{v}**" for k, v in stats.items()])

        embed_content.add_field(name="", value=f"<t:{int(time())}:R>")
        print(f"{title:_<50}" if title else '', ", ".join([f"{k.replace(' ', '-')}={v}" for k, v in stats.items()]))
        async with ClientSession() as s:
            webhook = Webhook.from_url(url, session=s)
            await webhook.send(embed=embed_content)
