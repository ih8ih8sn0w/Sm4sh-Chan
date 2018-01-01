import os
import discord
import asyncio
from .utils import checks
from .utils.dataIO import fileIO
from discord.ext import commands
from random import choice as rndchoice
from __main__ import send_cmd_help

class MOTD:
	"""MOTD"""
	def __init__(self, bot):
		self.bot = bot
		self.motds = fileIO("data/motd/motd.json", "load")

	@commands.group(pass_context=True)
	@checks.is_owner()
	async def motd(self, ctx):
		"""Test"""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@motd.command(name="add", pass_context=True)
	async def _motd_add(self, ctx, *, msg: str):
		#TODO Check if it's already in the DB
		self.motds.append(msg)
		fileIO("data/motd/motd.json", "save", self.motds)

	@motd.command(aliases=["remove"], name="delete", pass_context=True)
	async def _motd_delete(self, ctx, *, msg: str):
		#TODO Check if it's already in the DB
		self.motds.remove(msg)
		fileIO("data/motd/motd.json", "save", self.motds)

	@motd.command(name="clear", pass_context=True)
	async def _motd_clear(self, ctx):
		fileIO("data/motd/motd.json", "save",  [])

	async def change_presence():
		while self is self.bot.get_cog("MOTD"):
			await self.bot.change_presence(game=discord.Game(name=rndchoice(self.motds)))
			await asyncio.sleep(30)

def check_folders():
    if not os.path.exists("data/motd"):
        print("Creating data/motd folder...")
        os.makedirs("data/motd")

def check_files():
    f = "data/motd/motd.json"
    if not fileIO(f, "check"):
        print("Creating empty motd.json...")
        fileIO(f, "save", [])

def setup(bot):
	check_folders()
	check_files()
	n = MOTD(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.change_presence())
	bot.add_cog(n)