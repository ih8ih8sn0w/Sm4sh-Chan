import discord
from discord.ext import commands
import random
import time

class Personality:
	def __init__(self, bot):
		self.bot = bot
		self.bot.add_message_modifier(message_mod)

	def __unload(self):
		self.bot.remove_message_modifier(message_mod)

def message_mod(msg : str):
	if "some credits" in msg:
		return "Here, take your money, pleb."
	else:
		return msg

def setup(bot):
	n = Personality(bot)
	bot.add_cog(n)