memberrolename='NAME OF MEMBER ROLE'
muterolename='NAME OF MUTED ROLE'
BOT_TOKEN = 'BOT TOKEN GOES HERE'

from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import discord
import asyncio
import tinydb
import time

bot = commands.Bot(command_prefix='!')

bot.remove_command('help')

mutes={}

db=tinydb.TinyDB('db.json')
query=tinydb.Query()
@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(activity=discord.Game(name='!help'))
    for i in db:
        ids = i['id'].split(' ')
        server = bot.get_guild(int(ids[1]))
        member = server.get_member(int(ids[0]))
        print(server,member)
        
        mute_role = discord.utils.get(member.guild.roles, name=muterolename)
        member_role = discord.utils.get(member.guild.roles, name=memberrolename)

        if not member_role in member.roles:
            await member.add_roles(member_role)
        if mute_role in member.roles:
            await member.remove_roles(mute_role)

        db.remove(query.id==(str(member.id)+' '+str(server.id)))
    
@bot.command()
async def mute(ctx, user: str, mtime: int):
    member = ctx.message.mentions[0]
    mute_role = discord.utils.get(member.guild.roles, name=muterolename)
    member_role = discord.utils.get(member.guild.roles, name=memberrolename)

    if ctx.message.author.guild_permissions.administrator:
        if db.search(query.id == (str(member.id)+' '+str(member.guild.id))) == []:
   
            await ctx.send(embed=discord.Embed(title=member.name+' was muted for '+str(mtime)+' seconds',color=0x00FF00))

            db.insert({'id':(str(member.id)+' '+str(member.guild.id)), 'expires':time.time()+mtime})
            print('db record inserted')

            await member.add_roles(mute_role)
            await member.remove_roles(member_role)
            print('changed roles')

            if mtime>0:
                print('beginning asyncio.sleep('+str(mtime)+')')
                await asyncio.sleep(mtime)
                print('waited successfully')
                if not member_role in member.roles:
                    await member.add_roles(member_role)
                if mute_role in member.roles:
                    await member.remove_roles(mute_role)
            print('gave back roles')
            if db.search(query.id==(str(member.id)+' '+str(member.guild.id))) != []:
                await ctx.send(embed=discord.Embed(title=member.name+'\'s mute has expired',color=0x00FF00))
            db.remove(query.id==(str(member.id)+' '+str(member.guild.id)))
            print('db record removed')
        else:
            await ctx.send(embed=discord.Embed(title=member.name+' could not be muted, because they are already muted. You can use `!unmute @user` to unmute them, so you can mute them again',color=0x00FF00))
    else:
        await ctx.send(embed=discord.Embed(title='You must be an administrator to use this command',color=0xFF0000))

@bot.command()
async def unmute(ctx,user: str):
    if ctx.message.author.guild_permissions.administrator:
        member=ctx.message.mentions[0]
        mute_role = discord.utils.get(member.guild.roles, name=muterolename)
        member_role = discord.utils.get(member.guild.roles, name=memberrolename)
        if not member_role in member.roles:
            await member.add_roles(member_role)
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
        db.remove(query.id==(str(member.id)+' '+str(member.guild.id)))
        print('db record removed')
        await ctx.send(embed=discord.Embed(title=member.name+' was unmuted',color=0x00FF00))
    else:
        await ctx.send(embed=discord.Embed(title='You must be an administrator to use this command',color=0xFF0000))

@bot.command()
async def help(ctx):
    embed=discord.Embed(
        title='mutebot Help',
        color=0x0000FF
        )
    embed.add_field(name='`!mute @user minutes`',value='mutes user for the specified number of minutes.\n Example: `!mute @testuser 10`',inline=False)
    embed.add_field(name='`!unmute @user`',value='unmutes the user if they are already muted.\n Example: `!unmute @testuser`',inline=False)
    embed.add_field(name='`!help`',value='displays this help message',inline=False)
    await ctx.send(embed=embed)


bot.run(BOT_TOKEN, bot=True, reconnect=True)

#NOTE: if the bot goes offline ever, anyone who is muted will stay muted until unmuted manually or bot comes back online
