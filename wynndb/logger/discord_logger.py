from __future__ import annotations
import traceback

from aiohttp import ClientSession
import discord

from wynndb import Config
from . import ConsoleLogger


class DiscordLogger:  # NOTE: i hate how this class looks
    """For exceptions needed to be sent to discord to be logged and reported to the developer."""

    def __init__(self, config: Config, console_logger: ConsoleLogger) -> None:
        self._config = config
        self._console_logger = console_logger

    async def exception(self, message: str, exception: None | BaseException = None) -> None:
        self._console_logger.exception(message)
        await self._send_to_discord(message, exception)

    async def error(self, message: str, exception: None | BaseException = None) -> None:
        await self._send_to_discord(message, exception)

    async def _send_to_discord(self, message: str, exc: None | BaseException) -> None:
        async with ClientSession() as s:
            hook = discord.Webhook.from_url(self._config.issues_webhook, session=s)
            if exc is None:
                await hook.send(f"Caught exception: {message}")
            else:
                await hook.send(embed=self._get_embed(message, exc))

    def _get_embed(self, message: str, exc: BaseException) -> discord.Embed:
        tb = f"`{exc}` ```{''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))}```"
        tb = tb[:1024]
        return discord.Embed(
                title="Caught exception",
                description=message,
                color=discord.Colour.red()
        ).add_field(name="Traceback", value=tb)
