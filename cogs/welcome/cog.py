import asyncio

import discord
from discord.ext.commands import Cog

from .models import WelcomeConfig
from .views import WelcomeView, ConfirmView


class WelcomeCog(Cog):
    """
    This cog contains code to manage the new user experience.
    """
    def __init__(self, bot):
        self.bot = bot

    welcome_group = discord.app_commands.Group(name="welcome", description="Commands relating to welcoming new users.")

    @welcome_group.command(
        name="set_welcome",
        description="Sets the welcome config for this server."
    )
    @discord.app_commands.guild_only()
    @discord.app_commands.checks.has_permissions(administrator=True)
    @discord.app_commands.describe(
        welcome_channel="The channel to send welcome messages in.",
        recruit_channel="The channel for recruitment discussions to happen in.",
        grant_role="The role to grant to those interested in joining.",
        recruiter_role="The role that all recruiters have.",
        message=(
                "The message you would like to be publicly displayed to users when they join. "
                "(Use {mention} anywhere you would like to mention the new user)"
        ),
    )
    async def set_welcome(
            self,
            inter: discord.Interaction,
            welcome_channel: discord.TextChannel,
            recruit_channel: discord.TextChannel,
            grant_role: discord.Role,
            recruiter_role: discord.Role,
            message: str):
        # Check if a welcome config exists for the current guild
        conf = await WelcomeConfig.objects.filter(guild_id=inter.guild_id).aexists()

        channel = inter.channel
        view_val = False

        if conf:
            view = ConfirmView()
            msg = await inter.response.send_message(
                content="Are you sure you want to overwrite the current config?",
                view=view,
                ephemeral=True
            )

            await view.wait()

            view_val = view.value

            if not view_val:
                return await inter.edit_original_response(content="Welcome config not overwritten.", veiw=None)

        conf_dict = {
            "guild_id": inter.guild_id,
            "channel_id": welcome_channel.id,
            "recruit_channel_id": recruit_channel.id,
            "grant_role_id": grant_role.id,
            "recruiter_role_id": recruiter_role.id,
            "message": message
        }

        conf = await WelcomeConfig.objects.aupdate_or_create(
            guild_id=inter.guild_id,
            defaults=conf_dict
        )

        if view_val:
            return await inter.edit_original_response(content="Welcome config overwritten.", view=None)
        return await inter.response.send_message(
            content="Welcome config saved!",
            ephemeral=True
        )

    @discord.app_commands.command(
        name="join",
        description="Add yourself to the recruitment channel."
    )
    @discord.app_commands.guild_only()
    async def join(self, inter: discord.Interaction):
        pass

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        conf = WelcomeConfig.objects.filter(guild_id=member.guild.id)

        if not await conf.aexists():
            return

        conf = await conf.afirst()

        fmt = {"mention": member.mention}
        formatted = conf.message.format(**fmt)

        channel = member.guild.get_channel(conf.channel_id)
        role = member.guild.get_role(conf.grant_role_id)

        await asyncio.sleep(10)

        if len(member.roles) == 1:
            view = WelcomeView(member, role)
            msg = await channel.send(formatted, view=view)
            view.set_message(msg)
        return


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))


async def teardown(bot):
    await bot.remove_cog(WelcomeCog)
