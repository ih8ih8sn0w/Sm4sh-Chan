import os
import asyncio
import time
import discord
from random import randint
from .utils import checks
from .utils.dataIO import fileIO
from discord.ext import commands

class Chatroulette:
	def __init__(self, bot):
		self.bot = bot
		self.muted = fileIO("data/economy/roulette.json", "load")

	@commands.command(aliases=["russianroulette"], pass_context=True, no_pm=True)
	@checks.is_owner()
	async def roulette(self, ctx):
		"""Bet your virtual life with the russian roulette!

		1 chance out of 6 to earn a well-deserved 10 minutes mute. Or money. Or... something."""
		user = ctx.message.author
		rand = randint(0, 5)
		multiplier = 2
		economy = self.bot.get_cog('Economy')
		mod = self.bot.get_cog('Mod')
		if not economy.bank.account_exists(user):
			await self.bot.say("<@{}>, you do not have a bank account yet. Use the command .bank register to open an account.".format(user.id))
			return
		if rand > 1:
			economy.bank.deposit_credits(user, economy.settings[ctx.message.server.id]["PAYDAY_CREDITS"] * multiplier)
			await self.bot.say("You get to live another day. Enjoy your {} credits, you earned them.".format(economy.settings[ctx.message.server.id]["PAYDAY_CREDITS"] * multiplier))
		else:
			self.bot.add_message_modifier(message_mod)
			await ctx.invoke(mod.server_mute, user=user, reason="Roulette")
			self.muted.append({"ID" : user.id, "FUTURE" : int(time.time()+ 10)})
			fileIO("data/economy/roulette.json", "save", self.muted)
			self.bot.remove_message_modifier(message_mod)

	async def check_mutes(self, ctx):
		to_unmute = []
		mod = self.bot.get_cog('Mod')
		for mute in self.muted:
			if mute["FUTURE"] <= int(time.time()):
				try:
					await ctx.invoke(mod.server_unmute, user=discord.Member(id=mute["ID"]))
					to_unmute.append(mute)
				except:
					to_unmute.append(mute)
		for mute in to_unmute:
			self.muted.remove(mute)
		if to_unmute:
			fileIO("data/economy/roulette.json", "save", self.muted)
			print("COUILLE")
			await asyncio.sleep(5)

def message_mod(msg: str):
	if "User has been muted in this server." in msg:
		return "Too bad, the roulette is rigged. It happens !"
	else:
		return msg

def check_files():
	f = "data/economy/roulette.json"
	if not fileIO(f, "check"):
		print("Creating empty roulette.json...")
		fileIO(f, "save", [])

def setup(bot):
	check_files()
	n = Chatroulette(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.check_mutes())
	bot.add_cog(n)