import discord
from discord.ext import commands

from utils.loggers import get_logger

logger = get_logger(__name__)


class AdminCommands(commands.Cog):
    """Cog containing classic chat commands for admin purposes"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sd'], hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        Commands the bot to shut down.
        """
        logger.critical(f"Bot shutdown called by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
        print(f"Bot shutdown called by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
        await ctx.send("Bot shutting down!")
        return exit(0)


class CoreCog(commands.Cog):
    """Cog containing classic and slash commands."""
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    def __base_embed(self, *args, **kwargs):
        """
        Returns a basic embed to be used for core command responses when needed. All kwargs are passed directly
        to the embed constructor.
        :param args:
        :param kwargs:
        :return:
        """
        embed = discord.Embed(**kwargs)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.with_static_format('png'))
        embed.set_thumbnail(url=self.bot.user.avatar.with_static_format('png'))

        return embed

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        """Just a test command."""
        return await ctx.send("Pong!")

    @discord.app_commands.command(name="about")
    async def about(self, i: discord.Interaction):
        """Displays general information about the bot."""

        # Define bot info
        app_info = await self.bot.application_info()
        owner = f'@{app_info.owner.name}'
        link = 'https://github.com/colcrunch/ceres'
        about_text = "Ceres is a bot written specifically for Fancypants Inc."

        embed = self.__base_embed(title=f'About {self.bot.user.name}', description=about_text)
        embed.add_field(name="Bot Owner", value=owner, inline=True)
        embed.add_field(name='Bot Author', value="@colcrunch", inline=True)
        embed.add_field(name='GitHub', value=link, inline=False)

        return await i.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(CoreCog(bot))


async def teardown(bot):
    await bot.remove_cog(AdminCommands)
    await bot.remove_cog(CoreCog)
