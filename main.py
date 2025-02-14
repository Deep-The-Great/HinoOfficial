# Team Hino

from discord.ext import tasks
from itertools import cycle
import discord
import os
import datetime
import asyncio
from discord.ext import commands
from discord.utils import get
import time
import random
import aiohttp
import json


client = commands.Bot(command_prefix="h!")

# Events

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"on {len(client.guilds)} servers | h!help"
    ))
    print("Ready")


#invite

@client.command()
async def invite(ctx):
  masked_link = discord.Embed(
    title = '**Invite this bot to your server**',
    description = '**[Invite](https://discord.com/api/oauth2/authorize?client_id=765460752718102528&permissions=2080631927&scope=bot)**',
    color = discord.Colour.teal()
    )
  await ctx.send(embed=masked_link)
  pass

# Help
client.remove_command('help')
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.green())

    embed.set_author(name='CATEGORY LIST')

    embed.add_field(name='**MODERATION CATEGORY**', value='Type h!help moderation for more details', inline=False)
    embed.add_field(name='**TICKET CATEGORY**', value='Type h!help ticket for more details', inline=False)
    embed.add_field(name='**FUN**', value='Type h!help fun for more details', inline=False)
    embed.add_field(name='**OTHER**', value='Type h!help other for more details', inline=False)
    #embed.add_field(name='**ADMIN**', value='```invite |```')
    embed.set_footer(text='Made by Team Hino')

    await ctx.send(embed=embed)

@help.command()
async def moderation(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name = "purge (no.)", value = "Clear the text in channel in server")
    embed.add_field(name = "kick (user)", value = "Kick the user from the server")
    embed.add_field(name = "ban (user)", value = "Ban the user from the server")
    embed.add_field(name = "Unban (user)[only name no @ sign]", value = "Unban the user from the server" )
    embed.add_field(name = "nuke", value = "Nuke a channel in the server")
    embed.add_field(name = "addrole (user) (role-name)", value = "Add a role to a mention user")
    embed.add_field(name = "removerole (user) (role-name)", value = "Remove a role from a user")

    await ctx.send(embed=embed)

@help.command()
async def ticket(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name = "setupticket", value = "Setup the ticket by the bot")
    embed.add_field(name = "openticket", value = "Open a ticket for purpose")
    embed.add_field(name = "closeticket", value = "Close a ticket")

    await ctx.send(embed=embed)

@help.command()
async def fun(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name = "howgay (user)", value = "Howgay the user" )
    embed.add_field(name = "cat", value = "Send a random picture of Cat")
    embed.add_field(name = "meme", value = "Send a random meme")

    await ctx.send(embed=embed)

@help.command()
async def other(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name = "say (message)", value = "Send the message mentioned by the user")
    embed.add_field(name = "invite", value = "Invite the bot to your server")

    await ctx.send(embed=embed)
   


        
# Setup ticket

@client.command(pass_content = True)
async def setupticket(ctx):
    embed = discord.Embed(colour=discord.Colour.green())

    # Ticket System
    embed.description= 'Do you want me to setup my ticket system? Type y for yes and n for no'
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', timeout=30)
    if msg.content == "yes" or msg.content == "y":
        guild = ctx.guild
        support_perms = discord.Permissions(administrator=True)
        await guild.create_role(name='Support Team', permissions=support_perms)
        await ctx.guild.create_category('tickets')
        embed.description= """I created ``Support Team`` role for my ticket system.\nI created ``TICKETS`` category for my ticket system."""
        embed.set_footer(text='Made by Hino Team')

        await ctx.send(embed=embed)
    else:
        await ctx.send('**Setup for ticket system has not done**')


# Ping

@client.command()
async def ping(ctx):
    embed = discord.Embed(colour = discord.Colour.green())
    embed.add_field(name='Pong!', value=f'my ms is {round(client.latency *1000)}', inline=False)

    await ctx.send(embed=embed)

# Howgay

@client.command(aliases=['howgay', 'gay'])
async def _howgay (ctx, *, person):
    embed = discord.Embed(colour= discord.Colour.green())
    responses = ['10%',
                 '25%',
                 '50%',
                 '60%',
                 '70%',
                 '80%',
                 '90%',
                 '100%']
    embed.description = f'**{person} is {random.choice(responses)} gay** :rainbow:'
    embed.set_footer(text='Made by Team Hino')

    await ctx.send(embed = embed)

@_howgay.error
async def _howgay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour= discord.Colour.red())
        embed.add_field(name=':x: **Howgay Error**\n', value=' ㅤ\n``howgay {mention}``', inline=False)
        embed.set_footer(text='Made by Team Hino')

        await ctx.send(embed = embed)

# Purge

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount : int):
    embed = discord.Embed(colour=discord.Colour.green())
    await ctx.channel.purge(limit=amount)
    embed.description= f'**Purge**\nI purged {amount}'

@purge.error
async def _purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Purge Error**\n', value=' ㅤ\n``purge {amount}``', inline=False)
        embed.set_footer(text='Made by Team Hino')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Purge Error**\n', value=' ㅤ\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino')

        await ctx.send(embed = embed)



# Kick member

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member , * , reason=None):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name=f'kicked- {member}', value=f'Reason: {reason}', inline=False)

    await member.kick(reason=reason)
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Kick Error**\n', value=' ㅤ\n``kick {@mention}``', inline=False)
        embed.set_footer(text='Made by Team Hino')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Kick Error**\n', value=' ㅤ\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino')

        await ctx.send(embed=embed)

# Ban

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member , * , reason=None):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name=f'Banned- {member}', value=f'Reason: {reason}\nhttps://i.imgur.com/8d6Oakt.gif', inline=False)

    await member.ban(reason=reason)
    await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Ban Error**\n', value=' ㅤ\n``ban {@mention}``', inline=False)
        embed.set_footer(text='Made by Team Hino')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Purge Error**\n', value=' ㅤ\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino') 
    
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def ben(ctx, content, member : discord.Member , * , reason=None, id):
    if content == 'ed':
        guild = ctx.guild
        await guild.ban(discord.Object(id=id))
        await ctx.send(f'banned <@!{id}>')

# Unban member

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name,user.discriminator) == (member_name, member_discriminator):
            embed = discord.Embed(colour=discord.Colour.green())
            embed.description = f'**Unbanned- {user} **'

            await ctx.guild.unban(user)
            await ctx.send(embed=embed)
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Unban Error**\n', value=' ㅤ\n``unban {user#}``', inline=False)
        embed.set_footer(text='Made by Team Hino')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Unban Error**\n', value=' ㅤ\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino') 
        
        await ctx.send(embed=embed)

#say

@client.command()
async def say(ctx, *, say):
    embed= discord.Embed(colour=discord.Colour.green())
    embed.description = f"{say}"
    embed.set_footer(text='Made by Team Hino')

    await ctx.send(embed=embed)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Say Error**\n', value=' ㅤ\n``say {something}``', inline=False)
        embed.set_footer(text='Made by Team Hino')

        await ctx.send(embed=embed)

# Nuke channel

@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    await ctx.send("Nuking this channel")
    time.sleep(1)
    channel_id = ctx.channel.id
    channel = client.get_channel(channel_id)
    new_channel = await ctx.guild.create_text_channel(name=channel.name, topic=channel.topic, overwrites=channel.overwrites, nsfw=channel.nsfw, category=channel.category, slowmode_delay=channel.slowmode_delay, position=channel.position)
    await channel.delete()
    await new_channel.send("Nuked this channel.\nhttps://imgur.com/LIyGeCR")

@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Nuke Error**\n', value=' ㅤ\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino') 
        
        await ctx.send(embed=embed)

    


# Add Role

@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, mention):
    role = discord.utils.get(user.guild.roles, name=f'{mention}')
    await user.add_roles(role)
    await ctx.send(f'''I added {user} '{mention}' role!''')

@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Addrole Error**\n', value=' ㅤ\n``addrole {@role}+{@mention}``', inline=False)
        embed.set_footer(text='Made by Team Hino')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: ** Addrole Error**\n', value=' ㅤ\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino') 
        
        await ctx.send(embed=embed)

# Remove Role

@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, mention):
    role = discord.utils.get(user.guild.roles, name=f'{mention}')
    await user.remove_roles(role)
    await ctx.send(f'''I removed {user} '{mention}' role!''')

@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Removerole Error**\n', value=' ㅤ\n``removerole {@role}+{@mention}``', inline=False)
        embed.set_footer(text='Made by Team Hino')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Unban Error**\n', value='\n``You dont have permission to perform this action``', inline=False)
        embed.set_footer(text='Made by Team Hino') 

        await ctx.send(embed=embed)


# Ticket

@client.command()
async def openticket(ctx, *, content):
    embed = discord.Embed(colour=discord.Colour.green())
    y = 0
    for guild in client.guilds:
        for role in guild.roles:
            if "Support Team" in str(role):
                y = y + 1
    if y == 0:
        await guild.create_role(name="Support Team")
    x = 0
    for guild in client.guilds:
        for category in guild.categories:
            if "tickets" in str(category):
                x = x + 1
                tickets_category = category
    if x == 0:
        tickets_category = await ctx.guild.create_category("tickets")
    author = ctx.author.name.replace(" ", "-")
    author = author.lower()
    for guild in client.guilds:
        for channel in guild.text_channels:
            if "ticket-"+author in channel.name:
                 embed.description= 'You already made a ticket!'
                 return
    admin_role = get(guild.roles, name="Support Team")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(send_messages=True,read_messages=True),
        admin_role: discord.PermissionOverwrite(send_messages=True,read_messages=True)
    }
    ticket_channel = await ctx.guild.create_text_channel(name="ticket-"+author, topic=content, overwrites=overwrites, nsfw=None, category=tickets_category, slowmode_delay=None,position=None)
    embed.description= "You successfully created a ticket! in <#"+str(ticket_channel.id)+">"
    await ctx.send(embed=embed)

    embed.description= "**New ticket**\n\n<@"+str(ctx.author.id)+"> Opened ticket with reason "+str(content)
    await ticket_channel.send(embed=embed)

@openticket.error
async def openticket_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Ticket Error**\n', value=' ㅤ\n``ticket {Reason/Subject}``', inline=False)
        embed.set_footer(text='Made by Team Hino')

        await ctx.send(embed=embed)

# Close a ticket

@client.command()
async def closeticket(ctx):
    channel_id = ctx.channel.id
    channel = client.get_channel(channel_id)
    if "ticket" in channel.name:
        await ctx.send("Are you sure that you want to close the ticket?\ny or yes to close or write any other message to stay it open")
        msg = await client.wait_for('message', timeout=30)
        if msg.content == "yes" or msg.content == "y":
            await ctx.send("closing")
            await channel.delete()
        else:
            await ctx.send("Np")

# Cat

@client.command()
async def cat(ctx):
    embed = discord.Embed(colour=discord.Colour.green(), title="""Here's a cat""")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://aws.random.cat/meow') as r:
            res = await r.json()
            embed.set_image(url=res['file'])

            await ctx.send(embed=embed)

# Meme

@client.command()
async def meme(ctx):
    embed = discord.Embed(colour=discord.Colour.green(), title="""Here's a meme""")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])

            await ctx.send(embed=embed)


client.run(os.getenv('TOKEN'))
