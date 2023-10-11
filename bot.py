import datetime
import os

import discord
from discord.ext.commands import Bot

from utils.loggers import get_logger


class CeresBot(Bot):
    def __init__(self, *args, **kwargs):
        """
        Set up the bot class.
        """
        # Store discord-related data
        intents = discord.Intents.all()
        self.token = os.getenv("BOT_TOKEN", None)

        # Record start time for bot, used for calculating uptime.
        self.started = datetime.datetime.utcnow()

        # Set up logging
        self.logger = get_logger(__name__)

        super().__init__(
            command_prefix=os.getenv("CLASSIC_COMMAND_PREFIX", "!"),
            pm_help=None,
            description="A sane discord bot.",
            status=discord.Status.online,
            activity=discord.Activity(name="for new people.", type=discord.ActivityType.watching),
            intents=intents
        )

    def run(self, **kwargs):
        super().run(self.token)

    async def setup_hook(self) -> None:
        """
        Set up the bot. Load extensions, handle extensions failing to load, setup slash commands.
        """
        extensions = os.getenv("EXTENSIONS", "").replace(" ", "").split(",")
        print(extensions)

        for extension in extensions:
            try:
                await self.load_extension(f"cogs.{extension}.cog")
            except Exception as e:
                self.logger.critical(f"{extension} failed to load. Exception:")
                self.logger.critical(e)
                print(f"{extension} failed to load. Check the discord logs for more information.")
            else:
                self.logger.info(f"{extension} loaded.")
                print(f"{extension} loaded.")

        main_guild = discord.Object(id=os.getenv("MAIN_GUILD_ID", "0"))
        self.tree.copy_global_to(guild=main_guild)
        await self.tree.sync(guild=main_guild)

    async def on_ready(self) -> None:
        """
        Print and log a message to indicate that the bot is online and ready.
        """
        self.logger.info(f"Bot started! (U: {self.user.name} I: {self.user.id})")
        print(f"Bot started! (U: {self.user.name} I: {self.user.id})")
