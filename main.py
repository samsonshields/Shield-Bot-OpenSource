import nextcord
import os
import random
from nextcord.ext.commands import MissingPermissions
from humanfriendly import InvalidTimespan
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import CommandInvokeError
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands import BotMissingPermissions
from nextcord.ext.commands import MissingRole
from nextcord.ext.commands import MemberNotFound
from nextcord.ext.commands import errors
import json
from nextcord.ext import commands, tasks
from nextcord.utils import get
from itertools import cycle
from nextcord.utils import find
import nextcord.utils
import humanfriendly
import datetime
from setuptools import Command

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


def get_prefix(client, message):
    if not message.guild:
        return "$"

    try:
        with open('./prefixes.json', "r") as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

    except nextcord.DiscordException:
        return "$"

client = commands.Bot(command_prefix=get_prefix, activity = nextcord.Game(name=f'| $help'), intents = intents, help_command=None)
    
@client.event 
async def on_ready():
    print('Shield Bot Dist is started and online') 

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
      with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

      prefix = prefixes[str(message.guild.id)]
      embed = nextcord.Embed(description=f'Current server prefix is \'{prefix}\' \nFor more, use the \'{prefix}help\' command', color=0x3498db)
      await message.channel.send(embed=embed)
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('./prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    guild_owner = client.get_user(int(guild.owner.id))
    embed = nextcord.Embed(title=f'Thanks for choosing Shield Bot!', description=f'My default prefix is \'$\', however this can be changed by using the \'$prefix\' command', color=0x3498db)
    embed.add_field(name="Commands List", value=f'[Our website](https://bit.ly/3y1pX9R)')
    embed.add_field(name="Help/ Support", value=f'[Support Server](https://discord.gg/BYU5GqUVek)')
    channel = await guild_owner.create_dm()
    await channel.send(embed=embed)

@client.event
async def on_guild_remove(guild):
    with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('./prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.purge(limit=1)
        emoji = '<:ShieldError:996559560691155024>'
        embed = nextcord.Embed(description=f'{emoji} You don\'t have permission to do this', color=0xFC3400)
        await ctx.channel.send(embed=embed, delete_after=5)
        return
    elif isinstance(error, CommandNotFound):
        emoji = '<:ShieldError:996559560691155024>'
        embed = nextcord.Embed(description=f'{emoji} This command does not exist', color=0xFC3400)
        await ctx.channel.send(embed=embed, delete_after=5)
        return
    elif isinstance(error, InvalidTimespan):
        emoji = '<:ShieldError:996559560691155024>'
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(description=f'{emoji} You are missing required time argument', color=0xFC3400)
        await ctx.channel.send(embed=embed, delete_after=15)
        return
    elif isinstance(error, MissingRequiredArgument):
        emoji = '<:ShieldError:996559560691155024>'
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(description=f'{emoji} You are missing a part of the command!', color=0xFC3400)
        await ctx.channel.send(embed=embed, delete_after=5)
        return
    elif isinstance(error, MissingRole):
        emoji = '<:ShieldError:996559560691155024>'
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(description=f'{emoji} User does not have that role', color=0xFC3400)
        await ctx.channel.send(embed=embed, delete_after=10)
        return
    elif isinstance(error, BotMissingPermissions):
        emoji = '<:ShieldError:996559560691155024>'
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(description=f'{emoji} I do not have the required permissions to run this command', color=0xFC3400)
        await ctx.channel.send(embed=embed)
        return
    elif isinstance(error, MemberNotFound):
        emoji = '<:ShieldError:996559560691155024>'
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(description=f'{emoji} Desired search query was not found', color=0xFC3400)
        await ctx.channel.send(embed=embed)
        return
    else:
        emoji = '<:ShieldError:996559560691155024>'
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(description=f'{emoji} Error in command. Please try again', color=0xFC3400)
        await ctx.channel.send(embed=embed, delete_after=10)
        print(error)


@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    if commands.has_permissions(administrator=True):
        with open('./prefixes.json', 'r') as f:
            prefixes = json.load(f)
    
        prefixes[str(ctx.guild.id)] = prefix
    
        with open('./prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        emoji = '<:ShieldError:996559560691155024>'
        embed = nextcord.Embed(description=f'{emoji} Prefix successfully changed to {prefix}', color=0x60C546, timestamp=ctx.message.created_at)
        await ctx.channel.send(embed=embed)
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
async def config(ctx):
    await ctx.channel.purge(limit=1)
    website = 'https://bit.ly/3y1pX9R'
    setup_instructions = f'• To get Shield Bot up and running in your server, you might need to do some setup. For any questions, head over to our website: {website}\n • In order to ensure the safety of your server, most of our commands only work if the person using them has moderator and or administrator permissions.\n • Additionally, you should make sure all of your current members with moderator and administrator permissions can be trusted. Shield Bot is a powerful tool which should only be used by trustworthy members.'
    embed = nextcord.Embed(title='Thanks for adding Shield Bot to your server!', description=f'{setup_instructions}', color=0x3498db, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")
    await ctx.channel.send(embed=embed)

@client.command(pass_context=True)
async def help(ctx):
    with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefix = prefixes[str(ctx.guild.id)]
    await ctx.channel.purge(limit=1)
    embed = nextcord.Embed(title=f'Server: {ctx.guild}', description=f'The current prefix in this server is \'{prefix}\'', color=0x3498db, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")
    embed.add_field(name="Help and Support", value="[List of commands](https://dev--shield-bot-website.prodsamshields.autocode.gg/commands.html)")
    embed.add_field(name="Shield Bot website", value=f'[Our website](https://bit.ly/3y1pX9R)')
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(moderate_members=True)
async def ban(ctx, member: nextcord.Member, *,     reason='None'):  
    if commands.has_permissions(administrator=True) or commands.has_permissions(moderate_members=True):
        if member.guild_permissions.administrator or member.guild_permissions.moderator:
            await ctx.send(f'You can\'t do that! That member is a moderator/ administrator!')
            return
        embed = nextcord.Embed(title='Shield Bot', description=f'You have been banned from {ctx.guild} for reason: {reason}', color=0x3498db, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        channel = await member.create_dm()
        await channel.send(embed=embed)
        emoji = '<:ShieldCheck:996559064295284826>'
        embed = nextcord.Embed(description=f'{emoji} {member} has been banned for reason: {reason}', color=0x60C546, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed)
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(moderate_members=True)
async def unban(ctx, *, member):
    emoji = '<:ShieldCheck:996559064295284826>'
    embed = nextcord.Embed(description=f'{emoji} {member} has been unbanned', color=0x60C546, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    if commands.has_permissions(administrator=True) or commands.has_permissions(moderate_members=True):
        for ban_entry in banned_users:
            user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(embed=embed, delete_after=5)
            return
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=2):
    if commands.has_permissions(administrator=True):
        await ctx.channel.purge(limit=amount)
    else:
        return

@client.command()
async def info(ctx):
    embed = nextcord.Embed(title='Shield Bot', description='Hi, im Shield Bot! For help with specific commands, please use the $help and $help associated commands.', color=0x3498db, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")
    channel = ctx.channel
    await channel.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(moderate_members=True)
async def kick(ctx, member : nextcord.Member, *,   reason='None'):
    if commands.has_permissions(administrator=True) or commands.has_permissions(moderate_members=True):
        if member.guild_permissions.administrator or member.guild_permissions.moderator:
            await ctx.send(f'You can\'t do that! That member is a moderator/ administrator!')
            return
        embed = nextcord.Embed(title='Shield Bot', description=f'You have been kicked from {ctx.guild} for reason: {reason}', color=0x3498db, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        channel = await member.create_dm()
        await channel.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.channel.purge(limit=1)
        emoji = '<:ShieldCheck:996559064295284826>'
        embed = nextcord.Embed(description=f'{emoji} {member} has been kicked for reason: {reason}', color=0x60C546, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await ctx.channel.send(embed=embed, delete_after=5)
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, member : nextcord.Member, *, role : nextcord.Role):
    emoji = '<:ShieldCheck:996559064295284826>'
    embed = nextcord.Embed(title='Shield Bot', description=f'{emoji} {member} has been added to role: {role}', color=0x60C546, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")
    if commands.has_permissions(administrator=True):
        await member.add_roles(role)
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed, delete_after=5)
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx, member : nextcord.Member, role : nextcord.Role):
    emoji = '<:ShieldCheck:996559064295284826>'
    embed = nextcord.Embed(escription=f'{emoji} {member} has been removed from role: {role}', color=0x60C546, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")

    if commands.has_permissions(administrator=True):
        await member.remove_roles(role)
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed, delete_after=5)
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, message=None):
    if commands.has_permissions(administrator=True):
        await ctx.channel.purge(limit=1)
        await ctx.send(message)
    else:
        return

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: nextcord.Member=None, time=None, *, reason=None):
    if commands.has_permissions(administrator=True) or commands.has_permissions(moderate_members=True):
        if member.guild_permissions.administrator or member.guild_permissions.moderator:
            await ctx.send(f'You can\'t do that! That member is a moderator/ administrator!')
            return
        time = humanfriendly.parse_timespan(time)
        embed = nextcord.Embed(title=None, description=f'You have been timed out in {ctx.guild} for {time} minutes | Reason: {reason}', color=0x3498db, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await member.timeout(nextcord.utils.utcnow() + datetime.timedelta(minutes=time), reason=reason)
        channel = await member.create_dm()
        await channel.send(embed=embed)
        await ctx.channel.purge(limit=1)
        emoji = '<:ShieldCheck:996559064295284826>'
        embed = nextcord.Embed(description=f'{emoji} {member} has been timed out for {time} minutes | Reason: {reason}', color=0x60C546, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await ctx.channel.send(embed=embed)
    else:
        return
#-------------------------------------------------

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(moderate_members=True)
async def timein(ctx, member: nextcord.Member=None, time=None, *, reason=None):
    if commands.has_permissions(administrator=True) or commands.has_permissions(moderate_members=True):
        embed = nextcord.Embed(title='Shield Bot', description=f'You have been removed from timeout in {ctx.guild} | Reason: {reason}', color=0x3498db, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await member.timeout(None, reason=reason)
        channel = await member.create_dm()
        await channel.send(embed=embed)
        await ctx.channel.purge(limit=1)
        emoji = '<:ShieldCheck:996559064295284826>'
        embed = nextcord.Embed(description=f'{emoji} {member} has been removed from timeout | Reason: {reason}', color=0x60C546, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await ctx.channel.send(embed=embed)
    else:
        return

#-------------------------------------------------

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changenick(ctx, member: nextcord.Member, *, nick):

    if commands.has_permissions(administrator=True):
        if member.guild_permissions.administrator or member.guild_permissions.moderator:
            await ctx.send(f'You can\'t do that! That member is a moderator/ administrator!')
            return
        await member.edit(nick=nick)
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(title='Shield Bot', description=f'Your nickname in {ctx.guild} was changed to \'{nick}\'', color=0x3498db, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        channel = await member.create_dm()
        await channel.send(embed=embed)
      
        embed = nextcord.Embed(title='Shield Bot', description=f'Nickname was changed for {member.mention}', color=0x60C546, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await ctx.channel.send(embed=embed)
    
    else:
        return

@client.command()
async def randnum(ctx, min, max):
    min = int(min)
    max = int(max)
    number = random.randint(min, max)
    await ctx.send(f'Your random number between {min} and {max} is: {number}')

@client.command()
async def coinflip(ctx):
    roll = random.randint(1, 2)
    if roll == 1:
        await ctx.send('Heads!')
    elif roll == 2:
        await ctx.send('Tails!')
    else:
        return

@client.command()
async def website(ctx):
    website = 'https://bit.ly/3y1pX9R'
    embed = nextcord.Embed(description=f'Shield Bot website: {website}', color=0x3498db, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"ID: {ctx.message.id}")
    await ctx.channel.send(embed=embed)

@client.command()
async def poll(ctx, question, *options: str):

    emoji1 = '1️⃣'
    emoji2 = '2️⃣'
    emoji3 = '3️⃣'

    user = ctx.author
    color = user.top_role.color
    
    if len(options) == 1:
        embed = nextcord.Embed(title=f'{question}', description=f'{emoji1} {options}', color=color, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Asked by: {ctx.author}")
        message = await ctx.channel.send(embed=embed) 
        await message.add_reaction(emoji1)
    

    elif len(options) == 2:
        embed = nextcord.Embed(title=f'{question}', description=f'{emoji1} {options[0]}\n{emoji2} {options[1]}', color=color, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Asked by: {ctx.author}")
        message = await ctx.channel.send(embed=embed) 
        await message.add_reaction(emoji1)
        await message.add_reaction(emoji2)

    elif len(options) == 3:
        embed = nextcord.Embed(title=f'{question}', description=f'{emoji1} {options[0]}\n{emoji2} {options[1]}\n{emoji3} {options[2]}', color=color, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Asked by: {ctx.author}")
        message = await ctx.channel.send(embed=embed) 
        await message.add_reaction(emoji1)
        await message.add_reaction(emoji2)
        await message.add_reaction(emoji3)
    elif len(options) > 3:
      emoji_deny = '<:ShieldError:996559560691155024>'
      embed = nextcord.Embed(description=f'{emoji_deny} The maximum amount of options is 3', color=0xFC3400)
      await ctx.channel.purge(limit=1)
      await ctx.channel.send(embed=embed)
    
    else:
        denied = '<:ShieldError:996559560691155024>'
        embed = nextcord.Embed(description=f'{denied} You must have at least one option', color=0xFC3400)
        await ctx.channel.send(embed=embed) 

@client.command()
async def whois(ctx, member: nextcord.Member = None):
    color = member.top_role.color
    if not member:  # if member is not mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = nextcord.Embed(colour=color, timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar)
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.set_footer(text=f"ID: {ctx.message.id}")

    embed.add_field(name="User ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Account Created On:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Joined {ctx.guild} On:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Current Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    await ctx.send(embed=embed)


@client.command()
async def banner(ctx, member: nextcord.Member = None):
    if not member:
        member = ctx.message.author
    req = await client.http.request(nextcord.http.Route("GET", "/users/{uid}", uid=member.id))
    banner_id = req["banner"]
    extension = ()
    if banner_id:
        if banner_id.startswith('a_'):
            extension = '.gif'
        else:
            extension = '.png'
        user = ctx.author
        color = user.top_role.color
        embed = nextcord.Embed(colour=color, timestamp=ctx.message.created_at, title=f'{member}\'s banner')
        embed.set_image(url=f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}{extension}?size=1024")
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    else:
        emoji = '<:ShieldError:996559560691155024>'
        embed = nextcord.Embed(colour=0x3498db, timestamp=ctx.message.created_at, description=f'{emoji} {member} does not have an active banner!')
        embed.set_footer(text=f'Requested by {ctx.author}')
        embed.set_footer(text=f"ID: {ctx.message.id}")
        await ctx.send(embed=embed, delete_after=10)


@client.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
    if commands.has_permissions(administrator=True):
        if not seconds:
            await ctx.channel.edit(slowmode_delay=0)
            emoji = '<:ShieldCheck:996559064295284826>'
            embed = nextcord.Embed(description=f'{emoji} Slowmode removed', color=0x60C546)
            await ctx.send(embed=embed)
        elif seconds > 21600:
          emoji = '<:ShieldError:996559560691155024>'
          embed = nextcord.Embed(description=f'{emoji} Slowmode cannot exceed 21,600 seconds', color=0x60C546)
          await ctx.send(embed=embed)
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            emoji = '<:ShieldCheck:996559064295284826>'
            embed = nextcord.Embed(description=f'{emoji} Slowmode set to {seconds} seconds', color=0x60C546)
            await ctx.send(embed=embed)
    else:
        return

client.run(your token here)
