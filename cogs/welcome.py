import discord
import logging
import os
import asyncio

from .utils import checks
from .utils.dataIO import fileIO
from discord.ext import commands
from __main__ import send_cmd_help

class Welcome:
	"""Welcome"""
	def __init__(self, bot):
		self.bot = bot
		self.settings = fileIO("data/welcome/settings.json", "load")
		self.data = {"CHANNEL": self.settings["CHANNEL"], "ROLE": self.settings["ROLE"], "PASSWORD": self.settings["PASSWORD"]}

	@commands.group(name="welcome", pass_context=True, no_pm=True)
	@checks.mod_or_permissions()
	async def _welcome(self, ctx):
		"""Welcome"""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@_welcome.command(name="setwaitroom", pass_context=True)
	async def welcome_setwaitroom(self, ctx, channel: discord.Channel):
		if self.data["CHANNEL"] == channel.id:
			await self.bot.say("The waitroom channel is already set to <#{}>. Stop looking at my face already and get to work, you big dummy!".format(channel.id))
		else:
			self.data["CHANNEL"] = channel.id
			fileIO("data/welcome/settings.json", "save", self.data)
			await self.bot.say("The waitroom is now set to <#{}>.".format(channel.id))
		if self.data["ROLE"] is None:
				await self.bot.say("Oh, and please be careful, no role is set for the newcomers! I-It's not like I want ***you*** to set one or anything... *Don't get the wrong idea...*")
		if self.data["PASSWORD"] is None:
			await self.bot.say("Don't forget to add a password while you're at it.")

	@_welcome.command(name="setdefaultrole", pass_context=True)
	async def welcome_setdefaultrole(self, ctx, role: discord.Role):
		if self.data["ROLE"] == role.id:
			await self.bot.say("The default role is already set to **{}**. -*sigh*- What would you do without me.".format(role.name))
		else:
			self.data["ROLE"] = role.id
			fileIO("data/welcome/settings.json", "save", self.data)
			await self.bot.say("The default role is now set to **{}**.".format(role.name))
		if self.data["CHANNEL"] is None:
			await self.bot.say("Oh, and please give a look at the waitroom. It's not set yet!")
		if self.data["PASSWORD"] is None:
			await self.bot.say("Don't forget to add a password while you're at it.")

	@_welcome.command(name="setpassword", pass_context=True)
	async def welcome_setpassword(self, ctx, password: str):
		if self.data["PASSWORD"] == password:
			await self.bot.say("This password is already in use, boi.")
		else:
			self.data["PASSWORD"] = password.lower()
			fileIO("data/welcome/settings.json", "save", self.data)
			await self.bot.say("The new password is now set to **{}**.".format(password))
		if self.data["CHANNEL"] is None:
			await self.bot.say("However, setting a password without specifying the waitroom is a bit useless, so please don't forget to do it.")
		if self.data["ROLE"] is None:
			await self.bot.say("Also, don't forget to specify a default role.")

	async def on_message(self, message):
		if message.channel.id != self.data["CHANNEL"]:
			return
		if message.author.bot:
			return
		if self.data["ROLE"] is None:
			return
		if self.data["PASSWORD"] in message.content.lower():
			try:
				for role in message.server.roles:
					if role.id == self.data["ROLE"]:
						userrole = role
						break
				if userrole in message.author.roles:
					return
				await self.bot.add_roles(message.author, userrole)
				await self.bot.delete_message(message)
				await self.bot.send_message(message.author, "Welcome to {}, hope you enjoy it!".format(message.server.name))
			except:
				await self.bot.send_message(message.channel, ("No."))

	async def on_member_join(self, member):
		message = await self.bot.send_message(member.server.get_channel(self.settings["CHANNEL"]), "Hello <@{}>, and welcome to the exciting world of Smash 4 Modding !\nPlease read the first post and <#177915412426653696> before posting.".format(member.id))
		delay = 60
		if delay == -1:
			return

		await asyncio.sleep(delay)
		await self.bot.delete_message(message)


def check_folders():
	if not os.path.exists("data/welcome"):
		print("Creating data/welcome folder...")
		os.makedirs("data/welcome")

def check_files():
	f = "data/welcome/settings.json"
	if not fileIO(f, "check"):
		print("Creating empty settings.json")
		fileIO(f, "save", {"CHANNEL": None, "ROLE": None, "PASSWORD": None})

def setup(bot):
	check_folders()
	check_files()
	bot.add_cog(Welcome(bot))