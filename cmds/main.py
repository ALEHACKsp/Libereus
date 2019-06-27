import discord
from discord.ext import commands
from core.scripts import dcEscape
from core.classes import ExtensionBase
import time, datetime
# from core.classes import Whitelist

# new_whitelist = Whitelist()
class Main(ExtensionBase):
	"""Core commands for bot."""
	@commands.command()
	async def ping(self, ctx):
		"""Delay between Discord and the websocket latency."""
		t = time.perf_counter()
		await ctx.trigger_typing()
		t2 = time.perf_counter()
		await ctx.trigger_typing()

		bot = round((t2 - t) * 1000)
		ws = int(self.bot.latency * 1000)
		await ctx.send(f'Pong!\nLatency: `{bot}ms` Websocket: `{ws}ms`')
			
	@commands.command()
	async def say(self, ctx, *, content: str):
		"""Say something."""
		msg = content.strip() #Remove whitespaces
		await ctx.send(dcEscape(msg, 'ping'))
		#TODO: Check perms before @everyone or @here

	# 給定天數 計算日期
	@commands.command()
	async def calcdate(self, ctx, day: int):
		"""Simple date calculate. <day: +- int>"""
		today = datetime.date.today()
		tdelta = datetime.timedelta(days=day)
		await ctx.channel.send(today + tdelta)

	# 指定使用者判斷是否超過指定天數
	@commands.command()
	async def checkdate(self, ctx, user: discord.Member, day: int):
		await ctx.channel.send("Checking......:scroll:")
		res_list = []
		for channel in self.bot.get_all_channels():
			if isinstance(channel, discord.TextChannel):
				channels = channel
				if channel.guild == ctx.guild:
					try:
						msg = await channels.history().get(author__name= user.name)
						msgdate = str(discord.utils.snowflake_time(msg.id))
						dt = datetime.date(int(msgdate[0:4]), int(msgdate[5:7]), int(msgdate[8:10]))
						today = datetime.date.today()
						res = today - dt
						if int(res.days) > abs(day):
							res_list.append("true")
						else:
							res_list.append("false")
					except AttributeError:
						pass
					except discord.errors.Forbidden:
						pass
						# await ctx.channel.send("Not enought permission")
		embed = discord.Embed(title="Check date status", color=0x5fe0b9)
		if 'false' not in res_list:
			embed.add_field(name="Result",value=":x:Kick that ass")
			await ctx.channel.send(embed=embed)
		else:
			embed.add_field(name="Result", value=":white_check_mark: Damn, this guy is fine!")
			await ctx.channel.send(embed=embed)

	
	@commands.command(enabled=False)
	async def whitelist(self, ctx, user: discord.Member):
		new_whitelist.white.append(user)
		new_whitelist.name.append(user.name)
		await ctx.send(f"Appended {user} to white list.")
	
	@commands.command(enabled=False)
	async def show_white(self, ctx):
		await ctx.send(new_whitelist.name)
		
def setup(bot):
	bot.add_cog(Main(bot))