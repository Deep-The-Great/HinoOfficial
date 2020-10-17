import discord
from discord.ext import commands
import datetime
import asyncio
import random
import os

client = commands.Bot(command_prefix=">")

@client.event
async def on_ready():
	print("Bot is ready")

@client.command()
async def help(ctx):
	await ctx.send("```hello sir```")

@client.command()
@commands.has_role("Snipers")
async def gstart(ctx, mins : int, * , prize: str):
    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60) 

    embed.add_field(name = "Ends At:", value = f"{end} UTC")
    embed.set_footer(text = f"Ends {mins} mintues from now!")

    my_msg = await ctx.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(mins*60)


    new_msg = await ctx.channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congratulations! {winner.mention} won {prize}!")

  


client.run(os.getenv('TOKEN'))