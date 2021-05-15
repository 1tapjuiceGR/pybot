import discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, has_permissions, MissingPermissions
import json
from asyncio import sleep

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

#Animated Bot Status 
async def status():
    while True:
        await client.wait_until_ready()
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='ᴀᴋᴜᴋʟᴏꜰᴏⓇɪᴛᴏꜱ#4184'))
        await sleep(5)
        await client.change_presence(activity=discord.Game(name="Made By Juice#1203"))
        await sleep(5)

@client.event
async def on_ready():
    print('Bot is online')
client.loop.create_task(status())


blacklist_words = ["https://", "discord.gg/"]
#Blacklisted words Event
@client.event
async def on_message(msg):
    for word in blacklist_words:
        if word in msg.content:
            await msg.delete()

        await client.process_commands(msg)


#Event that gives role when someone joins
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Insert role name')
    await client.add_roles(member, role)

#Whois Command
@client.command()
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.red())
    embed.add_field(name = "Id", value = member.id , inline = True )
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

#Clear/Purge Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} Messages Cleared by {ctx.author.mention}')

#Kick command
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f'{member.mention} Has Been kicked', mention_author=True)


#ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f'{member.mention} Has Been Banned', mention_author=True)

#Unban command
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#mute command (you must make a muted role,and replace "role id below,with yours")
@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(Replace with your muted role id)

    await member.add_roles(muted_role)

    await ctx.send(member.mention + f" has been muted by {ctx.author.mention}")

#unmute command (you must make a muted role,and replace "role id below,with yours")
@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(Replace with your muted role id)

    await member.remove_roles(muted_role)

    await ctx.send(member.mention + f" Has been unmuted by {ctx.author.mention}")

#Channel Lock Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"Channel locked by {ctx.author.mention}")

#Channel Unlock Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"Channel unlocked by {ctx.author.mention}")



client.run('Your Bot Token here')
