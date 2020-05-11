memberrolename='member'
muterolename='m'

from discord.ext import commands
import discord
import asyncio
import tinydb
import time
from threading import Thread
from flask import Flask
import os

# =====================================================================================
app = Flask('')# start of the keepalive script

@app.route('/')
def home():
    return "I'm online<br>mutebot"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()# from https://bit.ly/3clliSR because I didnt think of this workaround myself
# =====================================================================================

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
   
            await ctx.send(embed=discord.Embed(title=member.name+' was muted for '+str(mtime)+' minutes',color=0x00FF00))

            db.insert({'id':(str(member.id)+' '+str(member.guild.id)), 'expires':time.time()+(mtime*60)})
            print('[mute] db record inserted')

            await member.add_roles(mute_role)
            await member.remove_roles(member_role)
            print('[mute] changed roles')

            if mtime>0:
                print('[mute] beginning asyncio.sleep('+str(mtime*60)+')')
                await asyncio.sleep(mtime*60)
                print('[mute] waited successfully')
                if not member_role in member.roles:
                    await member.add_roles(member_role)
                if mute_role in member.roles:
                    await member.remove_roles(mute_role)
            print('[mute] gave back roles')
            if db.search(query.id==(str(member.id)+' '+str(member.guild.id))) != []:
                await ctx.send(embed=discord.Embed(title=member.name+'\'s mute has expired',color=0x00FF00))
            db.remove(query.id==(str(member.id)+' '+str(member.guild.id)))
            print('[mute] db record removed')
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
        print('[unmute] db record removed')
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
    print('[help] help message sent')
    await ctx.send(embed=embed)

keep_alive()
bot.run(os.environ.get('TOKEN'), bot=True, reconnect=True)

#NOTE: if the bot goes offline ever, anyone who is muted will stay muted until unmuted manually or bot comes back online
