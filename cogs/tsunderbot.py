import discord
import random
import os
import time
from discord.ext import commands
from cogs.utils import checks
from .utils.dataIO import dataIO

class TsunderBot:
	"""Control the queen of Tsundere"""
	def __init__(self, bot):
		self.bot = bot
		self.cogdir = "data/tsunderbot/"
		self.settings = dataIO.load_json("data/tsunderbot/settings.json")
		self.operator = 0
		self.operators = ["Binary", "Ruby", "Morse", "Virus", "Python", "Array"]

	@commands.command(pass_context=True)
	@checks.mod_or_permissions()
	async def randomize(self, ctx):
		random.seed(time.time())
		self.operator = random.randint(0, len(self.operators)-1)
		self.settings["operator"] = self.operator
		directory = self.get_operator_folder() + "Avatars/"
		avatars = os.listdir(directory)
		if len(avatars) < 2:
			rand = 0
		else:
			rand = random.randrange(0, len(avatars)-1)
		f = open(directory + avatars[rand], "rb")
		read_data = f.read()
		await self.bot.edit_profile(self.bot.settings.password, avatar=read_data)
		f.close()
		await self.bot.say("Done")
		dataIO.save_json("data/tsunderbot/settings.json", self.settings)

	@commands.command(no_pm=False, pass_context=True)
	async def bio(self):
		info = dataIO.load_json(self.get_operator_folder() + "info.json")

		embed = discord.Embed(colour=info["COLOR"])
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.add_field(name="Current Operator", value=info["NAME"])
		embed.add_field(name="Personality", value=info["TYPE"], inline=False)
		embed.add_field(name="Measurements", value=info["MEASUREMENTS"], inline=False)
		embed.add_field(name="Bio", value=info["BIO"], inline=False)
		embed.set_footer(text=info["FOOTER"])
		await self.bot.say(embed=embed)

	def get_operator_folder(self):
		return self.cogdir + self.operators[self.operator] + "/"

def check_folders():
	if not os.path.exists("data/tsunderbot"):
		print("Creating data/tsunderbot folder...")
		os.makedirs("data/tsunderbot")

def check_files():
	if not os.path.isfile("data/tsunderbot/settings.json"):
		print("Creating empty settings.json...")
		dataIO.save_json("data/tsunderbot/settings.json", {})

def setup(bot):
	check_folders()
	check_files()
	bot.add_cog(TsunderBot(bot))