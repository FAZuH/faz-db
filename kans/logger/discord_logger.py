from aiohttp import ClientSession
import discord
from kans import ConfigT


class DiscordLogger:

    def __init__(self, config: ConfigT) -> None:
        self._config = config

    async def success(self, message: str) -> None:
        """Logs a success message. Used for successful operations."""
        message = f"{message}"
        await self._send_to_discord(message)

    async def exception(self, message: str) -> None:
        """Errors that needs to be logged and sent to discord. Used for handled issues that doesn't cause the program to stop."""
        message = f"{message}"
        await self._send_to_discord(message)

    async def error(self, message: str) -> None:
        """Errors that needs to be logged and sent to discord. Used for unhandled issues that causes the program to stop.
        This method is hooked to exit events to log errors automatically."""
        message = f"{message}"
        await self._send_to_discord(message)

    async def _send_to_discord(self, message: str) -> None:
        """Sends a message to discord."""
        async with ClientSession() as s:
            hook = discord.Webhook.from_url(self._config["ISSUES_WEBHOOK"], session=s)
            await hook.send(content=message)
