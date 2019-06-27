from discord.ext import commands
from core.classes import ExtensionBase
from core.helper import cmderr
import discord
import typing

class DiscordActions(ExtensionBase, name="Discord Actions"):
	"""Actions in Discord, turned to commands."""
	@commands.group()
	async def channel(self, ctx):
		if ctx.invoked_subcommand: return
		await ctx.send("Guild's overall channel information. TODO")

	@channel.command()
	async def info(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]):
		"""Get a channel's info."""
		await ctx.send(f"#{channel.name}'s info. TODO")

	@channel.command()
	async def create(self, ctx, ctype: str, *, name: str):
		"""Creates a new channel."""
		# type check
		if ctype not in ('text', 'textchannel', 'text-channel', 'tc',
		 'voice', 'voicechannel', 'voice-channel','vc', 
		 'category', 'categorychannel', 'category-channel', 'cat'):
			await ctx.send(":x: Unknown channel type. Valid values are `text`, `voice` and `category`.")
			return
		elif ctype in ('textchannel', 'text-channel', 'tc'):
			ctype = 'text'
		elif ctype in ('voicechannel', 'voice-channel', 'vc'):
			ctype = 'voice'
		elif ctype in ('categorychannel', 'category-channel','cat'):
			ctype = 'category'
		# channel creation
		if ctype == 'text':
			channel = await ctx.guild.create_text_channel(name)
		elif ctype == 'voice':
			channel = await ctx.guild.create_voice_channel(name)
		elif ctype == 'category':
			channel = await ctx.guild.create_category(name)
		await ctx.send("Created channel <#{channelID}>".format(channelID = channel.id))
	@create.error
	async def errChannelCreate(self, ctx, err):
		await cmderr(ctx, err, 
			commands_errors_Forbidden='r'+'I have not enough permission to create a new channel. Please give `Manage Channel` permission to me and try again.',
			commands_errors_HTTPException='r'+"Creating the channel failed. Please try again later.")

	@commands.command()
	async def channelinfo(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]):
		"""Alias to `channel info` command."""
		cmd = self.bot.get_command('channel info')
		await ctx.invoke(cmd, channel)

def setup(bot):
	bot.add_cog(DiscordActions(bot))