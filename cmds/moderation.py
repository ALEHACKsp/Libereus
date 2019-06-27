from discord.ext import commands
from core.classes import ExtensionBase
import discord
import typing

class Moderation(ExtensionBase):
	"""Moderation commands."""
	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def lockdown(self, ctx, channels: commands.Greedy[discord.TextChannel] = None, reason: str = 'N/A'):
		"""Disable @everyone's permission to send message on given channel or current channel if not specified."""
		if channels is None:
			channels = [ctx.channel]
		for c in channels:
			await c.set_permissions(c.guild.default_role, send_messages=False, 
				reason="Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author))
			await c.send("🔒 Locked down this channel.")
		if not channels == [ctx.channel]:
			await ctx.send("Locked down {count} channel{s}.".format(count=len(channels), s='s' if len(channels)>1 else ''))
	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def unlock(self, ctx, channels: commands.Greedy[discord.TextChannel] = None, reason: str = 'N/A'):
		"""Reset @everyone's permission to send message on given channel or current channel if not specified."""
		if channels is None:
			channels = [ctx.channel]
		for c in channels:
			await c.set_permissions(c.guild.default_role, send_messages=None, 
				reason="Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author))
		await ctx.send("Unlocked {count} channel{s}.".format(count=len(channels), s='s' if len(channels)>1 else ''))

	# @commands.command()
	# @commands.has_permissions(manage_channels=True)
	# async def slowmode(self, ctx, channel: typing.Optional[discord.TextChannel] = None, seconds: int):
	# 	"""Set channel's slowmode delay."""
	# 	if not (0 > seconds > (60*60*6)):
	# 		await ctx.send(":x: The seconds are either too short or too long.")
	# 	if channel is None: channel = ctx.channel
	# 	channel.slowmode_delay = seconds
	# 	await ctx.send("✅ Set #{channel} channel with {sec}sec slowmode.".
	# 		format(channel = channels.name, s='s' if len(channels)>1 else '', sec=seconds))

def setup(bot):
	bot.add_cog(Moderation(bot))