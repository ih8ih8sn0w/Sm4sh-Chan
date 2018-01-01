import discord
import urllib
import json
from .utils import checks
from discord.ext import commands

class IP:
	"""Returns the IP"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@checks.is_owner()
	async def getIP(self, ctx):
		address = urllib.request.urlopen("http://ident.me").read().decode("utf-8")
		await self.bot.say("Public IP: {}".format(address))

def setup(bot):
	bot.add_cog(IP(bot))