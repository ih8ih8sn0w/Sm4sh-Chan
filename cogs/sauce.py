import os
import discord
import aiohttp
import shutil
from discord.ext import commands
from .utils import checks

class Sauce:
    """Owner only. Allows the owner to upload a cog from the chat."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def upload(self, ctx):
        """Allows you to upload a cog as an attachment.
        Example: [prefix]upload"""
        if not ctx.message.attachments:
            await self.bot.say("At *least* give me a file to upload.")
            return

        attachment = ctx.message.attachments[0]
        
        await self.bot.say(attachment['url'])
        with aiohttp.ClientSession() as session:
            async with session.get(attachment['url']) as response:
                test = await response.read()
                with open("./cogs/" + attachment['filename'], "wb") as f:
                    f.write(test)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def source(self, ctx, name: str):
        if not os.path.exists("./cogs/" + name):
            await self.bot.say("There is no cog with that name.")
            return
        await self.bot.send_file(ctx.message.channel, "./cogs/" + name)

    @commands.command(aliases=["delete"], pass_context=True)
    @checks.is_owner()
    async def remove(self, ctx, filepath: str):
        if not os.path.exists(filepath):
            await self.bot.say("The specified filepath is nonexistant.")
            return
        if os.path.isdir(filepath):
            await self.bot.say("You're about to delete a folder and all of its content. Are you sure about that?")
            answer = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
            if answer is None:
                await self.bot.say("Operation aborted.")
                return
            if answer.content.lower() != "yes":
                await self.bot.say("Operation aborted.")
                return
            shutil.rmtree(filepath)
            await self.bot.say("Directory removed.")
            return
        if os.path.isfile(filepath):
            os.remove(filepath)
            return




def setup(bot):
    n = Sauce(bot)
    bot.add_cog(n)