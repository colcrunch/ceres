import datetime
import os

import discord
from discord.ext.commands import Bot

from utils.loggers import get_logger


class CeresBot(Bot):

    def __init__(self, *args, **qwargs):
        intents = discord.Intents.all()

        self.token = os.getenv("BOT_TOKEN", None)
        self.started = datetime.datetime.utcnow()

        self.logger = get_logger(__name__)

        super().__init__(
            command_prefix=os.getenv("CLASSIC_COMMAND_PREFIX", "!"),
            pm_help=None,
            description="A sane discord bot.",
            status=discord.Status.online,
            activity=discord.Activity(name="Waiting to welcome people.", type=discord.ActivityType.custom),
            intents=intents
        )

        extensions = os.getenv("EXTENSIONS", "").split(",")

        for extension in extensions:
            try:
                self.load_extension(f"cogs.{extension}.cog")
            except Exception as e:
                self.logger.critical(f"{extension} failed to load. Exception:")
                self.logger.critical(e)
                print(f"{extension} failed to load. Check the discord logs for more information.")
            else:
                self.logger.info(f"{extension} loaded.")
                print(f"{extension} loaded.")

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        self.logger.info(f"Bot started! (U: {self.user.name} I: {self.user.id})")
        print(f"Bot started! (U: {self.user.name} I: {self.user.id})")
