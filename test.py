import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=">")

@client.event
async def on_ready():
	print("Bot is ready")

@client.command()
async def hello(ctx):
	await ctx.send("Hi")

client.run(os.getenv('BOT_TOKEN'))
