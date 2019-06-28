from discord.ext import commands
from core.classes import ExtensionBase
from core.helper import log, cmderr
import discord
from random import randint
import datetime

class Automod(ExtensionBase):
	"""Auto moderation commands."""
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def prunemembers(self, ctx, days: int, include_no_message: bool = False):
		"""Prune inactive member (i.e. no message sent) given an inactive interval(days, minimum 1).
		Note that join/pin system message will also be considered as user's message.
		"""
		if days == 0 and include_no_message:
			await ctx.send("Pruning members with no message...")
		elif days < 1:
			await ctx.send("Interval too short, minimum accepted interval is 1.")
			return
		elif days >= 1100:
			await ctx.send("Interval too long, please consider lowering it.")
			return
		no_activity_members = []
		inactive_members = []
		last_msgs = []
		status_msg_content = "Searching and collecting data, this could take some time..."
		status_msg = await ctx.send(status_msg_content)
		guild_members = ctx.guild.members
		for pos, member in enumerate(guild_members):
			if member.bot: continue
			for channel in ctx.guild.text_channels:
				try:
					history = await channel.history().get(author__id=member.id)
					if history is not None: last_msgs.append(history)
				except discord.errors.Forbidden:
					pass
			while len(last_msgs) > 1:
				if last_msgs[0].created_at > last_msgs[1].created_at: # message is older
					last_msgs.append(last_msgs[0]) # append to the last
				del last_msgs[0]
			last_msg = last_msgs[0] if last_msgs else None
			# for those didn't send a message
			if last_msg == None and include_no_message:
				no_activity_members.append(member)
			elif last_msg == None:
				continue
			if (datetime.datetime.now() - last_msg.created_at).days > days:
				inactive_members.append(member)
			last_msgs.clear()
			# Progress
			# if pos / len(guild_members) > 0.9:
			# 	await status_msg.edit(content = status_msg_content + "\n90%")
			# elif pos / len(guild_members) > 0.8:
			# 	await status_msg.edit(content = status_msg_content + "\n80%")
			# elif pos / len(guild_members) > 0.7:
			# 	await status_msg.edit(content = status_msg_content + "\n70%")
			# elif pos / len(guild_members) > 0.5:
			# 	await status_msg.edit(content = status_msg_content + "\n50%")
			# elif pos / len(guild_members) > 0.2:
			# 	await status_msg.edit(content = status_msg_content + "\n20%")
			# elif pos / len(guild_members) > 0.1:
			# 	await status_msg.edit(content = status_msg_content + "\n10%")
			# elif pos / len(guild_members) > 0.05:
			# 	await status_msg.edit(content = status_msg_content + "\n5%")
			if pos % 5 == 0:
				 await status_msg.edit(content = status_msg_content + "\n{percentage}%".
				 	format(percentage=round(pos/len(guild_members)*100)))
		# status report
		await status_msg.edit(content = status_msg_content + "done")
		if no_activity_members:
			await ctx.send(
				"User that have no message in the server:\n{ulist}".
				format(ulist='\n'.join(['- '+str(m) for m in no_activity_members])))
		if inactive_members:
			await ctx.send(
				"User that haven't send a message in {days} day{s}:\n{ulist}".
				format(days=days, s='s' if days>1 else '', 
					ulist='\n'.join(['- '+str(m) for m in inactive_members])))
		# Kicking
		rand = randint(1000, 9999)
		await ctx.send(
			"Are you sure want to kick those members?\nType `yes {rand}` or `(n)o` to cancel.".
			format(rand=rand))
		try:
			response = await self.bot.wait_for('message', 
				check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, 
				timeout=120.0)
		except TimeoutError:
			await ctx.send("Timeout reached, task cancelled.")
		response.content = response.content.lower()
		if response.content == f"yes {rand}":
			kick_status = await ctx.send("Kicking users...")
			for m in no_activity_members:
				log(content=f"Kicking {m} (no activity)")
				await ctx.guild.kick(m, 
					reason="Haven't send a single message in the server, requested by {member}.".
					format(member=ctx.author))
			for m in inactive_members:
				log(content=f'Kicking {m} (inactive)')
				await ctx.guild.kick(m, 
					reason="Haven't send a message in {days} days, requested by {member}.".
					format(days=days, member=ctx.author))
			await kick_status.edit(content="Kicked out {count} users.".
				format(count=len(no_activity_members)+len(inactive_members)))
		elif response.content in ('n', 'no'):
			await ctx.send("Task aborted.")
		elif response.content in ('c', 'cancel'):
			await ctx.send("Task cancelled.")
		else:
			await ctx.send("Invalid response, task cancelled.")
	@prunemembers.error
	async def errPrunemembers(self, ctx , err):
		await cmderr(ctx, err, 
			discord_Forbidden='r'+'I lack `Kick Members` permission.',
			discord_HTTPException='r'+'An error occured when kicking members. Please try again later.')
		pass

def setup(bot):
	bot.add_cog(Automod(bot))