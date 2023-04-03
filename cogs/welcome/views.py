import discord
from discord.ui import View


class ConfirmView(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.blurple)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()


class WelcomeView(View):
    def __init__(self, member: discord.Member, role: discord.Role):
        super().__init__(timeout=None)
        self.message = None
        self.member = member
        self.role = role

    def set_message(self, message: discord.Message):
        self.message = message

    @discord.ui.button(label="Lemme Join!", style=discord.ButtonStyle.green)
    async def join(self, iact: discord.Interaction, button: discord.ui.Button):
        if iact.user != self.member:
            return await iact.response.send_message(
                (
                    "You cant make that choice for someone else.\n"
                    "However, if you wish to join, simply run the `/join` command."
                ),
                ephemeral=True
            )

        if self.role in self.member.roles:
            return await iact.response.send_message("You are already in the recruitment channel!", ephemeral=True)
        elif "Member" in [role.name for role in self.member.roles]:
            return await iact.response.send_message("You can't join more than once!", ephemeral=True)

        await self.member.add_roles(self.role)
        await iact.response.send_message("You have been granted access to the recruitment channel!", ephemeral=True)

        return await self.message.edit(content=self.message.content, view=None)

    @discord.ui.button(label="Just vibin!", style=discord.ButtonStyle.blurple)
    async def reject(self, iact: discord.Interaction, button: discord.ui.Button):
        if iact.user != self.member:
            return await iact.response.send_message("You can't make that choice for someone else.", ephemeral=True)

        await iact.response.send_message(
            (
                "Enjoy your stay! If you change your mind just run the `/join` command "
                "to be added to the recruitment channel"
            ),
            ephemeral=True
        )

        return await self.message.edit(content=self.message.content, view=None)
