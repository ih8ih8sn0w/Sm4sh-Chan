import discord
import os
import time
import asyncio

from .utils import checks
from .utils.dataIO import fileIO
from discord.ext import commands
from __main__ import settings

class Slowmode:
		"""Slowmode"""
		def __init__(self, bot):
			self.bot = bot
			self.refresh = 0
			self.count = 0
			self.channel = None
			self.activated = False
			self.datas = fileIO("data/slowmode/slowmode.json", "load")

		@commands.command(aliases=["zawarudo", "theworld"], no_pm=True, pass_context=True)
		@checks.mod_or_permissions(manage_messages=True)
		async def slowmode(self, ctx, quantity: int = 0, duration: int = 0):
			"""Show these memelords who's the boss. First argument is the quantity of messages per user, second is for how long to wait before the quantity is reset. Duration is in seconds.

			Example:
			[p]slowmode 1 5"""

			if quantity is 0:
				if self.activated is True:
					self.bot.remove_listener(self.check_incoming_message, "on_message")
					await self.bot.say("Slowmode deactivated")
				return
			self.count = quantity
			self.refresh = duration
			self.channel = ctx.message.channel
			self.bot.add_listener(self.check_incoming_message, "on_message")
			self.activated = True
			await self.bot.say("Slowmode activated.")

		async def check_incoming_message(self, message):
			author = message.author
			new_count = 1
			future = int(time.time() + self.refresh)
			to_remove = []

			if message.channel != self.channel:
				return
				
			if message.author.bot or self.is_mod_or_superior(message):
					return
					
			for data in self.datas:
				if data["ID"] == author.id:
					to_remove.append(data)
					if data["REFRESH"] >= int(time.time()):
						future = data["REFRESH"]
						if data["COUNT"] >= self.count:
							new_count = data["COUNT"]
							await self.bot.delete_message(message)
						else:
							new_count = data["COUNT"] + 1
			for data in to_remove:
				self.datas.remove(data)
			self.datas.append({"ID": author.id, "COUNT": new_count, "REFRESH": future})
			fileIO("data/slowmode/slowmode.json", "save", self.datas)
			
		def is_mod_or_superior(self, obj):
				if isinstance(obj, discord.Message):
						user = obj.author
				elif isinstance(obj, discord.Member):
						user = obj
				elif isinstance(obj, discord.Role):
						pass
				else:
						raise TypeError('Only messages, members or roles may be passed')

				server = obj.server
				admin_role = settings.get_server_admin(server)
				mod_role = settings.get_server_mod(server)

				if isinstance(obj, discord.Role):
						return obj.name in [admin_role, mod_role]

				if user.id == settings.owner:
						return True
				elif discord.utils.get(user.roles, name=admin_role):
						return True
				elif discord.utils.get(user.roles, name=mod_role):
						return True
				else:
						return False

def check_folders():
	if not os.path.exists("data/slowmode"):
		print("Creating data/slowmode folder...")
		os.makedirs("data/slowmode")

def check_files():
	f = "data/slowmode/slowmode.json"
	if not fileIO(f, "check"):
		print("Creating empty slowmode.json...")
		fileIO(f, "save", [])

def setup(bot):
	check_folders()
	check_files()
	bot.add_cog(Slowmode(bot))