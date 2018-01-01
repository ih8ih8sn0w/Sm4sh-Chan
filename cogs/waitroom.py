import discord
import logging
import os

from .utils import checks
from .utils.dataIO import dataIO
from discord.ext import commands

class Waitroom:
	"""Waitroom"""
	def __init__(self, bot):
		self.bot = bot
		self.waitroom = "data/waitroom/waitroom.json"
		self.riceCog = dataIO.load_json(self.waitroom)
		self.defaultrole = "data/waitroom/defaultrole.json"
		self.roleset = dataIO.load_json(self.defaultrole)

	@commands.command(pass_context=True)
	@checks.admin_or_permissions(manage_server=True)
	async def setwaitroom(self, ctx, channel : discord.Channel):
		server = ctx.message.server
		if server.id not in self.riceCog:
			self.riceCog[server.id] = channel.id
			dataIO.save_json(self.waitroom,
							 self.riceCog)
		else:
			self.riceCog[server.id] = channel.id
			dataIO.save_json(self.waitroom,
							 self.riceCog)
		await self.bot.say("Succesfully changed the *Waitroom* "
						   "channel to {}".format(channel.name))


	@commands.command(pass_context=True)
	@checks.admin_or_permissions(manage_server=True)
	async def setdefaultrole(self, ctx, default_role):
		server = ctx.message.server
		count = 0
		for role in server.roles:
			if role.name.lower() == default_role.lower():
				default_role = role
				break
			else:
				count += 1

		if count == len(server.roles):
			await self.bot.say("Role does not exist on this server. "
							   "Please try again.")
			return
		if server.id not in self.roleset:
			self.roleset[server.id] = default_role.id
			dataIO.save_json(self.defaultrole,
							 self.roleset)
		else:
			self.roleset[server.id] = default_role.id
			dataIO.save_json(self.defaultrole,
							 self.roleset)
		await self.bot.say("Succesfully changed the default *role* to "
						   "{}!".format(default_role))

	async def on_message(self, message):
		author = message.author
		server = message.server
		channel = message.channel
		if message.server is None:
			return
		if message.author.bot:
			return
		if channel.id in self.riceCog[server.id]:
			default_role = self.roleset[server.id]
			if "ready to fight" in message.content.lower():
				try:
					for role in server.roles:
						if role.id == default_role:
							userrole = role
							break
					if userrole in author.roles:
						return
					await self.bot.add_roles(author, userrole)
					await self.bot.send_message(author, "Welcome to Smash 4 Modding, b-baka...")
					await self.bot.delete_message(message)
				except discord.errors.Forbidden:
					await self.bot.send_message(message.channel, "Try checking bot permissions! Not like I want you to or anything...")
				except:
					await self.bot.send_message(message.channel, "Try checking the role again!")
		else:
			await self.bot.send_message(message.channel, "You did not set the *Waitroom* channel yet! "
							   "To do so, do {}setwaitroom "
							   "[channel]!".format(prefix))
			await self.bot.send_message(message.channel, "Also, set the default role using {}"
							   "setdefaultrole [rolename]!".format(prefix))

def check_folder():
	if not os.path.exists("data/waitroom"):
		print("Creating data/waitroom folder")
		os.makedirs("data/waitroom")

def check_file():
	data = {}
	f = "data/waitroom/waitroom.json"
	if not dataIO.is_valid_json(f):
		print("Creating data/waitroom/waitroom.json")
		dataIO.save_json(f,
						 data)

def check_file1():
	data = {}
	f = "data/waitroom/defaultrole.json"
	if not dataIO.is_valid_json(f):
		print("Creating data/waitroom/defaultrole.json")
		dataIO.save_json(f,
						 data)


def setup(bot):
	check_folder()
	check_file()
	check_file1()
	bot.add_cog(Waitroom(bot))
