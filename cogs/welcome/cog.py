import discord
from discord.ext.commands import GroupCog


class WelcomeCog(GroupCog, group_name="welcome"):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="set_message",
        description="Sets the messages to be sent when a new user joins the guild."
    )
    @discord.app_commands.guild_only()
    @discord.app_commands.checks.has_permissions(administrator=True)
    @discord.app_commands.describe(
        pub_message="The message you would like to be publicly displayed to users when they join.",
        priv_message="The message you would like to be privately displayed to users when they join."
    )
    async def set_message(self, inter: discord.Interaction, pub_message: str, priv_message: str):
        print(pub_message)
        print(priv_message)
        return await inter.response.send_message("Messages set!", ephemeral=True)

    @discord.app_commands.command(
        name="set_channel",
        description="Sets the channel to welcome new users in."
    )
    @discord.app_commands.guild_only()
    @discord.app_commands.checks.has_permissions(administrator=True)
    @discord.app_commands.describe(
        welcome_channel="The channel to send welcome messages in."
    )
    async def set_channel(self, inter: discord.Interaction, welcome_channel: discord.TextChannel):
        print(welcome_channel.name, welcome_channel.id)
        return await inter.response.send_message(f"Channel set to {welcome_channel.mention}!", ephemeral=True)

    @discord.app_commands.command(
        name="set_role",
        description="Sets the role to be assigned to users when they interact with the private message."
    )
    @discord.app_commands.guild_only()
    @discord.app_commands.describe(
        role="The role to be assigned to the user if they interact with the private message."
    )
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def set_role(self, inter: discord.Interaction, role: discord.Role):
        print(role.name, role.id)
        return await inter.response.send_message(f"Role set to {role.mention}!", ephemeral=True)

    @GroupCog.listener()
    async def on_member_join(self, member: discord.Member):
        pass


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))


async def teardown(bot):
    await bot.remove_cog(WelcomeCog)