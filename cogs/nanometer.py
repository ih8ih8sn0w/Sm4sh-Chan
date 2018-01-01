import discord
from __main__ import settings

class Nanometer:
	"""For those times when you can't mesure how big Nano's ego is"""
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		if message.author.bot:
			return
		if "#blameum" in message.content.lower():
			try:
				await self.bot.add_reaction(message, ":UMJustRight:264044698459570176")
			except:
				await self.bot.send_message(message.channel, "This emote doesn't exist anymore.")

		if message.author.id == "72804736297873408":
			if message.channel.id != "179679912909602816":
				return
		if message.author.id == "140344593429430272":
			if "i'm mowjoh" in message.content.lower():
				try:
					await self.bot.add_reaction(message, ":mowjoh:345635965596991488")
				except:
					await self.bot.send_message(message.channel, "This emote doesn't exist anymore, I can't add it to Mowjoh-kun.")

def setup(bot):
	n = Nanometer(bot)
	bot.add_cog(n)