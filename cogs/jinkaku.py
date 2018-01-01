import os
import discord
import random
from discord.ext import commands
from shutil import copy2
from .utils import checks
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box
from __main__ import send_cmd_help

default_settings = {
	"current" : 0,
	"cycling" : False,
	"operators" : ["Binary", "Ruby", "Morse", "Virus", "Python", "Array"]
}

default_operator = {
	"nickname" : "Default",
	"color" : 4276545,
	"avatar_cycling" : False
}

operator_folder_struc = ["/Avatars", "/Quotes"]

class Jinkaku:
	def __init__(self, bot):
		self.bot = bot
		self.path = "data/jinkaku/"
		self.settings = dataIO.load_json("data/jinkaku/settings.json")
		self.bot.load_extension('cogs.personality')
	def __unload(self):
		#Perform some tasks here when unloading the cog.
		self.bot.unload_extension('cogs.personality')
		return

	def save_settings(self):
		dataIO.save_json(self.path + "/settings.json", self.settings)

	#Operators related commands
	@commands.group(name="operators", pass_context=True, no_pm=True)
	async def operators(self, ctx):
		"""Commands dealing with the operators."""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@operators.command(name="add", pass_context=True)
	@checks.is_owner()
	async def operators_add(self, ctx, name : str):
		"""Add an operator entry to Sm4sh-Chan.
		Created with defaults settings and no avatar.

		Example: add Felicia"""
		if len(name) >= 255:
			await self.bot.say("This filename is too long, stop fooling around.")
			return

		if os.path.exists(self.path + name) and name not in self.settings["operators"]:
			await self.bot.say("It appears there is already a folder for this operator but it is not listed. Checking it's integrity...")

			if not self.isValidOperator(name):
				self.bot.say("The operator is missing some key directories, attempting to fix it...")
			else:
				self.bot.say("Operator is valid, adding to the list...")

			try:
				self.settings["operators"].append(name)
				self.save_settings()
				await self.bot.say("Added to the list successfully.")
			except:
				await self.bot.say("Something happened during the process.")
		elif not os.path.exists(self.path + name) and name in self.settings["operators"]:
			await self.bot.say("It appears this operator is already in the list. However, there's no folder related to it.\nCreating a default one...")
			self.create_operator(name)
			await self.bot.say("Folder structure created successfully.")
		elif not os.path.exists(self.path + name) and name not in self.settings["operators"]:
			root = self.path + name
			self.settings["operators"].append(name)
			self.save_settings()
			self.create_operator(name)
			await self.bot.say("{} has been created successfully. Yay, yay~".format(name))
		else:
			await self.bot.say("There's already an operator with that name.")

	@operators.command(name="list")
	@checks.mod_or_permissions()
	async def operators_list(self):
		"""Lists all the operators available"""
		op_list = self.settings["operators"]

		if op_list:
			for page in op_list:
				await self.bot.say(box(page))
		else:
			await self.bot.say("There are no operators. This might cause some problems.")

	@operators.command(name="set", pass_context=True)
	@checks.is_owner()
	async def operators_set(self, ctx, name : str):
		self.settings["current"] = self.settings["operators"].index(name)
		self.save_settings()
		directory = self.path + name + "/Avatars/"
		avatars = os.listdir(directory)
		f = open(directory + avatars[0], "rb")
		try:
			result = await self.bot.edit_profile(avatar=f.read())
			copy2(self.path + name + "/personality.py", "cogs")
			self.bot.load_extension('cogs.personality')
		except:
			pass
		f.close()
		await self.bot.say(embed=self.initialize_operator())

	#Utilitaries
	def create_operator(self, name: str):
		self.create_operator_folder_structure(name)
		self.create_operator_default_settings(name)
		dataIO.save_json(self.path + name + "/Quotes/quotes.json", {})
		copy2(self.path + "personality.py", self.path + name)


	def create_operator_folder_structure(self, name: str):
		root = self.path + name 
		os.makedirs(root)
		for folder in operator_folder_struc:
			if not os.path.exists(root + folder):
				os.makedirs(root + folder)

	def create_operator_default_settings(self, name: str):
		root = self.path + name
		new_operator = default_operator
		new_operator["nickname"] = name
		dataIO.save_json(root + "/config.json", new_operator)

	def initialize_operator(self):
		name = self.settings["operators"][self.settings["current"]]
		root = self.path + name + "/"
		config = dataIO.load_json(root + "/config.json")
		embed = discord.Embed(title=config["nickname"], description="No description for now.", colour=config["color"])
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		return embed

	def isValidOperator(self, name: str):
		root = self.path + name
		for folder in operator_folder_struc:
			if not os.path.exists(root + folder):
				return False
			else:
				continue

def check_folders():
	if not os.path.exists("data/jinkaku"):
		os.makedirs("data/jinkaku")

def check_files():
	f = "data/jinkaku/settings.json"
	if not dataIO.is_valid_json(f):
		dataIO.save_json(f, default_settings)

def setup(bot):
	check_folders()
	check_files()
	n = Jinkaku(bot)
	bot.add_cog(n)