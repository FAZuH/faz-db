import os
from loguru import logger
from nextcord import Colour, Embed, SyncWebhook

from . import LOG_DIR


class Logger:

    _webhook_url: str

    @classmethod
    def setup(cls, webhook_url: str) -> None:
        cls._webhook_url = webhook_url

        logger.level(name="UNEXPECTED", no=45, color="<red>")

        logger.add(sink=cls.__critical_sink, level="CRITICAL", enqueue=True)
        logger.add(sink=cls.__unexpected_error_sink, level="UNEXPECTED", enqueue=True)
        logger.add(sink=cls.__error_sink, level="ERROR", enqueue=True)

        os.makedirs(LOG_DIR, exist_ok=True)
        log_file = os.path.join(LOG_DIR, "fazdb.log")
        logger.add(log_file, level="ERROR", rotation="10 MB", retention="10 days", compression="zip", enqueue=True)

    @classmethod
    def __critical_sink(cls, message: str) -> None:
        cls.__send_embed_to_webhook("CRITICAL ERROR", message, Colour.dark_red())

    @classmethod
    def __unexpected_error_sink(cls, message: str) -> None:
        cls.__send_embed_to_webhook("UNEXPECTED ERROR", message, Colour.red())
        
    @classmethod
    def __error_sink(cls, message: str) -> None:
        cls.__send_embed_to_webhook("ERROR", message, Colour.red())
        
    @classmethod
    def __send_embed_to_webhook(cls, title: str, description: str, colour: Colour | None = None) -> None:
        webhook = SyncWebhook.from_url(cls._webhook_url)
        webhook.send(embed=Embed(
            title=title,
            description=description,
            colour=colour
        ))
