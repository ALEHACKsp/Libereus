from discord.ext import commands
from core.classes import ExtensionBase
from core.helper import cmderr
import discord
import typing
from inspect import Parameter

class DiscordActions(ExtensionBase, name="Discord Actions"):
	"""Actions in Discord, turned to commands."""
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = 'N/A'):
		"""Kick user from the guild with an optional reason."""
		for m in members:
			await m.kick(reason="Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author))
		await ctx.send("✅ Kicked {count} user{s} from the guild.".format(count=len(members), s='s' if len(members)>1 else ''))

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = "N/A"):
		"""Ban user fron the guild with an optional reason."""
		for m in members:
			await m.ban(reason="Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author), delete_message_days=0)
		await ctx.send("🔨 Banned {count} user{s} from the guild.".format(count=len(members), s='s' if len(members)>1 else ''))

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def softban(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = "N/A"):
		"""Ban user fron the guild with an optional reason and then unban them."""
		for m in members:
			await m.ban(reason="(softban) Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author), delete_message_days=0)
			await m.unban(reason="(softban) Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author))
		await ctx.send("⚒ Soft-banned {count} user{s} from the guild.".format(count=len(members), s='s' if len(members)>1 else ''))

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def forceban(self, ctx, uids: commands.Greedy[int], reason: str = "N/A"):
		"""Froce-ban user not in the guild given thier id with an optional reason."""
		for uid in uids:
			user = await self.bot.fetch_user(uid)
			await ctx.guild.ban(user, reason="(forceban) Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author), delete_message_days=0)
		await ctx.send("🔨 Force-banned {count} user{s} from the guild.".format(count=len(uids), s='s' if len(uids)>1 else ''))

	@commands.group()
	async def channel(self, ctx):
		if ctx.invoked_subcommand is None:
			raise commands.errors.MissingRequiredArgument(Parameter("subcommand", Parameter.POSITIONAL_OR_KEYWORD))

	@channel.command()
	async def info(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel] = None):
		"""Get a channel's info."""
		if channel is None:
			channel = ctx.channel
		if isinstance(channel, discord.TextChannel):
			ctype = "Text Channel"
		elif isinstance(channel, discord.VoiceChannel):
			ctype = "Voice Channel"
		elif isinstance(channel, discord.CategoryChannel):
			ctype = "Category"
		else:
			ctype = "Unknown"
		await ctx.send("<#{cid}>\n**Name:** {name}\n**ID:** {cid}\n**Type:** {type}".
			format(name=channel.name, cid=channel.id, type=ctype))

	@channel.command()
	@commands.has_permissions(manage_channels=True)
	async def create(self, ctx, ctype: str, *, name: str):
		"""Creates a new channel.
		Supported channel types: 'text' | `textchannel` | `tc` | `voice` | `voicechannel` | `vc` | `category` | `categorychannel` | `cat`"""
		# type check
		if ctype in ('text', 'textchannel', 'text-channel', 'textchnl', 'tc'):
			ctype = 'text'
		elif ctype in ('voice', 'voicechannel', 'voice-channel', 'voicechnl', 'vc'):
			ctype = 'voice'
		elif ctype in ('category', 'categorychannel', 'category-channel', 'categorychnl', 'cat'):
			ctype = 'category'
		else:
			await ctx.send(":x: Unknown channel type. Valid values are `text`, `voice` and `category`.")
			return
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
			discord_Forbidden='r'+'I do not have the required permission to create a new channel. Please give me the `Manage Channel` permission and try again.',
			discord_HTTPException='r'+"Creating the channel failed. Please try again later.")

	@commands.command()
	async def channelinfo(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel] = None):
		"""Alias to `channel info` command."""
		await ctx.invoke(self.bot.get_command('channel info'), channel)
	@commands.command(aliases=["createchnl"])
	async def createchannel(self, ctx, ctype: str, *, name: str):
		"""Alias to `channel create` command."""
		await ctx.invoke(self.bot.get_command('channel create'), channel)

def setup(bot):
	bot.add_cog(DiscordActions(bot))