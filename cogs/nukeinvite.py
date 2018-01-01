import discord
from __main__ import settings

class NukeInvite:
	"""Nuke invites"""
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		if message.server.id != "177913628668723201":
			return
			
		if message.author.bot:
			return
		if self.is_mod_or_superior(message):
			return
		if "https://discord.gg/" in message.content.lower():
			try:
				owner = discord.utils.get(self.bot.get_all_members(),
                                  id=self.bot.settings.owner)
				await self.bot.delete_message(message)
				await self.bot.send_message(message.author, "Invite links are prohibited in the server. If you wish to share one, ask a moderator or an administrator or send it by DMs.")
				await self.bot.send_message(owner, "<@{}> tried to send an invite in <#{}>.".format(message.author.id, message.channel.id))
			except:
				await self.bot.send_message(message.channel, ("Something happened."))

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

def setup(bot):
	bot.add_cog(NukeInvite(bot))