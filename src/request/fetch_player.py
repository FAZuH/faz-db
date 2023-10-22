from time import perf_counter
from typing import Set

from discord.ext import tasks

from .fetch_online import FetchOnline
from settings import FETCH_PLAYER_INTERVAL


class FetchPlayer:

    def __init__(self):
        pass
