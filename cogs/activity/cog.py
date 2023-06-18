import datetime

import discord
from discord.ext.commands import Cog

from .models import VoiceActivity


class VoiceActivityCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def __handle_connect(member: discord.Member) -> None:
        """
        Handle a user connecting to voice
        :param member:
        :return:
        """
        # First, check for unclosed activity records
        unclosed = VoiceActivity.objects.filter(guild_id=member.guild.id, user_id=member.id, disconnect_time=None)
        if await unclosed.aexists():
            # Handle unclosed activity
            async for u in unclosed:
                # We will assume that if the bot missed a disconnect event, the user would have been on for an hour.
                u.disconnect_time = u.disconnect_time + datetime.timedelta(hours=1)
                await u.asave()

        # Now that we have dealt with unclosed activity lets create an open activity record
        va = VoiceActivity(
            user_id=member.id,
            guild_id=member.guild.id,
        )
        await va.asave()
        return

    @staticmethod
    async def __handle_disconnect(member: discord.Member) -> None:
        """
        Handle a user disconnecting from voice.
        :param member: discord.Member
        :return:
        """
        now = datetime.datetime.utcnow()

        # First check that we have a record of this user joining voice.
        open = VoiceActivity.objects.filter(guild_id=member.guild_id, user_id=member.id).order_by("-connect_time")
        if not await open.aexists() or await open.afirst().disconnect_time is None:
            # If we get here we do not have record of the user joining.
            # Create and save a new record assuming a 1hr duration.
            va = VoiceActivity(
                user_id=member.id,
                guild_id=member.guild.id,
                connect_time=now-datetime.timedelta(hours=1),
                disconnect_time=now
            )
            await va.asave()
            return

        # Now that we have determined that there is an open activity record, lets close it.
        rec = await open.afirst()
        rec.disconnect_time = now
        await rec.asave()
        return

    @Cog.listener()
    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState):
        """
        Records voice state activity of discord users.
        :param member: discord.Member
        :param before: discord.VoiceState
        :param after: discord.VoiceState
        :return:
        """
        # Check if they were connected in the before state
        if before.channel is None:
            # They just connected!
            await self.__handle_connect(member)

        # If we get here, they were connected in the before state, now lets check the after state
        if after.channel is None:
            # They are disconnecting from voice
            await self.__handle_disconnect(member)

        # If we get here, the user is changing channels, and we don't want to do anything.
        return


async def setup(bot):
    await bot.add_cog(VoiceActivityCog(bot))


async def teardown(bot):
    await bot.remove_cog(VoiceActivityCog)
