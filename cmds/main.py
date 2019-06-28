import discord
from discord.ext import commands
from core.scripts import dcEscape
from core.classes import ExtensionBase
from random import randint
import time
import datetime

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

	@commands.command()
	async def calcdate(self, ctx, day: int):
		"""Add or subtract given day count by today and return."""
		today = datetime.date.today()
		tdelta = datetime.timedelta(days=day)
		await ctx.channel.send(today + tdelta)

	@commands.command()
	async def info(self, ctx):
		embed = discord.Embed(title="About Libereus", description="Moderation made easy.")
		embed.set_thumbnail(url="https://sc.s-ul.eu/FEYj6UQg")
		embed.add_field(name="Developers", value=
			"Tansc#8171 (<@!399471491017605120>)\nProladon#7525 (<@!149772971555160064>)\nNRockhouse#4157 (<@!140526642916229120>)", 
			inline=False)
		embed.add_field(name="Support Server", value="*None currently*" , inline=False)
		embed.add_field(name="Source", value="[Link](https://github.com/Tansc161/Libereus)", inline=True)
		embed.add_field(name="License", value="Mozilla Public License 2.0", inline=True)
		embed.set_footer(text="Made with ❤")

		await ctx.send(embed=embed)

	@commands.command(aliases=["ms"])
	async def minesweeper(self, ctx, width: int = 10, height: int = 10, difficulty: int = 30):
		"""Tired of moderation? Here is a mini minesweeper game for you!
		(PS: Don't show spoiler content to experience the fun!)
		"""
		grid = [['' for i in range(width)] for j in range(height)]
		num = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:']
		msg = ''

		if difficulty > 100:
			await ctx.send("Please enter difficulty in terms of percentage (1-100).")
			return
		if width <= 0 or height <= 0:
			await ctx.send("Invalid width or height value.")
			return
		if width * height > 160:
			await ctx.send("Your grid size is too big.")
			return
		if width * height <= 4:
			await ctx.send("Your grid size is too small.")
			return
		# set bombs in random location
		for y in range(0, height):
			for x in range(0, width):
				if randint(0, 100) <= difficulty:
					grid[y][x] = ':bomb:'

		# now set the number emojis
		for y in range(0, height):
			for x in range(0, width):
				if grid[y][x] != ':bomb:':
					grid[y][x] = num[sum([
						grid[y-1][x-1]==':bomb:' if y-1>=0 and x-1>=0 else False,
						grid[y-1][x]==':bomb:' if y-1>=0 else False,
						grid[y-1][x+1]==':bomb:' if y-1>=0 and x+1<width else False,
						grid[y][x-1]==':bomb:' if x-1>=0 else False,
						grid[y][x+1]==':bomb:' if x+1<width else False,
						grid[y+1][x-1]==':bomb:' if y+1<height and x-1>=0 else False,
						grid[y+1][x]==':bomb:' if y+1<height else False,
						grid[y+1][x+1]==':bomb:' if y+1<height and x+1<width else False
					])]

		# generate message
		for i in grid:
			for tile in i:
				msg += '||' + tile + '|| '
			msg += '\n'
		await ctx.send(msg)
		
def setup(bot):
	bot.add_cog(Main(bot))