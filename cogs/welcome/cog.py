import discord
from discord.ext.commands import GroupCog

from .views import ConfirmView


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
        doc_ref = self.bot.db.collection("welcome").document(f"{inter.guild.id}")

        data = {
            "priv_message": priv_message,
            "pub_message": pub_message
        }

        messages = doc_ref.get()
        view = None
        if messages.exists:
            message_dict = messages.to_dict()
            if "priv_message" in message_dict.keys():
                view = ConfirmView()
                await inter.response.send_message(
                    (
                        f"Welcome messages already set!\n"
                        f"Public:  `{message_dict['pub_message']}`\n"
                        f"Private: `{message_dict['priv_message']}`\n"
                        f"Are you sure you want to overwrite these messages?"
                    ),
                    view=view,
                    ephemeral=True
                )
                await view.wait()
                if view.value is None:
                    return await inter.edit_original_response(content="Timed out.", view=None)
                elif view.value is False:
                    return await inter.edit_original_response(content="Canceled.", view=None)

        doc_ref.set(data, merge=True)
        if view is not None:
            return await inter.edit_original_response(content="Messages set!", view=None)
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
        doc_ref = self.bot.db.collection("welcome").document(f"{inter.guild_id}")

        data = {
            "channel": welcome_channel.id
        }

        channel = doc_ref.get()
        view = None
        if channel.exists:
            channel_dict = channel.to_dict()
            if "channel" in channel_dict.keys():
                view = ConfirmView()
                await inter.response.send_message(
                    (
                        f"Welcome channel already set!\n"
                        f"Channel: {self.bot.get_channel(channel_dict['channel']).mention}\n"
                        f"Are you sure you want to change it?"
                    ),
                    view=view,
                    ephemeral=True
                )
                await view.wait()
                if view.value is None:
                    return await inter.edit_original_response(content="Timed out.", view=None)
                elif view.value is False:
                    return await inter.edit_original_response(content="Canceled.", view=None)

        doc_ref.set(data, merge=True)
        if view is not None:
            return await inter.edit_original_response(content=f"Channel set to {welcome_channel.mention}!", view=None)
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
        doc_ref = self.bot.db.collection("welcome").document(f"{inter.guild.id}")

        data = {
            "role": role.id
        }

        doc = doc_ref.get()
        view = None
        if doc.exists:
            doc_dict = doc.to_dict()
            if "role" in doc_dict.keys():
                view = ConfirmView()
                await inter.response.send_message(
                    (
                        f"Welcome role already set!\n"
                        f"Role: {inter.guild.get_role(doc_dict['role']).mention}\n"
                        f"Are you sure you want to change it?"
                    ),
                    view=view,
                    ephemeral=True
                )
                await view.wait()
                if view.value is None:
                    await inter.edit_original_response(content="Timed out.", view=None)
                if view.value is False:
                    await inter.edit_original_response(content="Canceled.", view=None)

        doc_ref.set(data, merge=True)
        if view is not None:
            return await inter.edit_original_response(content=f"Role changed to {role.mention}!", view=None)
        return await inter.response.send_message(f"Role set to {role.mention}!", ephemeral=True)

    @GroupCog.listener()
    async def on_member_join(self, member: discord.Member):
        pass


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))


async def teardown(bot):
    await bot.remove_cog(WelcomeCog)