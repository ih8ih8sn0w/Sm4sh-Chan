import discord
from discord.ext import commands
from random import choice as rndchoice
from .utils.dataIO import fileIO
from .utils import checks
import os

class Xsend:
    """Cross send.

    Allows you to send a message in a different channel.

    Example: [prefix]xsend #general pingas"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def xsend(self, ctx, channel: discord.Channel, *, msg: str):
        """Slap a user"""
        await self.bot.delete_message(ctx.message)
        await self.bot.send_message(channel, msg)

def setup(bot):
    n = Xsend(bot)
    bot.add_cog(n)