import discord
from discord.ext import commands
import nest_asyncio
import os
import random
import time
from os.path import exists
import subprocess
from time import sleep
from datetime import datetime
import asyncio
import openai
import json
from lxml import html
from lxml import etree
import requests
import threading
from threading import Thread
import cogs.themes
import schedule

#############################################################################################
######################          Global Initializations          #############################
#############################################################################################

intents = discord.Intents.all()
nest_asyncio.apply()
bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client(intents=intents)
blank = "‎"
defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

initial_extensions = ['cogs.help',
                      'cogs.themes',
                      'cogs.birthday',
                      'cogs.role',
                      'cogs.dev',
                      'cogs.ai',
                      'cogs.service',
                      #'cogs.tiktok', Retired due to being IP banned.
                      #'cogs.riot', Retired due to incompleteness/underuse of features
                      'cogs.events',
                      'cogs.qrcode',
                      'cogs.fun',
                      'cogs.moderation',
                      'cogs.vc',
                      'cogs.gifs',
                      #'cogs.warframe', Retired due to no solid API being available
                      'cogs.gm',
                      'cogs.dm',
                      'cogs.lyrics']

###########################################################

###########################################################

@bot.command(name="enable", hidden=True)
@commands.has_permissions(administrator = True)
async def enable(ctx, arg=None):
    if arg == None:
        errorEmbed = discord.Embed(color=red)
        errorEmbed.add_field(name=":x: Please specify a cog to add!",value="(use $cogs to view them all)")
        await ctx.reply(embed=errorEmbed)
    try:
        await bot.load_extension("cogs."+arg)
        successEmbed = discord.Embed(color=green)
        successEmbed.add_field(name=f":white_check_mark: {arg} Cog enabled!", value="Enjoy the functionality!")
        await ctx.reply(embed=successEmbed)
    except:
        errorEmbed = discord.Embed(color=red)
        errorEmbed.add_field(name=":x: That is not a valid Cog!",value="(use $cogs to view them all)")
        await ctx.reply(embed=errorEmbed)

@bot.command(name="disable", hidden=True)
@commands.has_permissions(administrator = True)
async def diable(ctx, arg=None):
    if arg == None:
        errorEmbed = discord.Embed(color=red)
        errorEmbed.add_field(name=":x: Please specify a cog to remove!",value="(use $cogs to view them all)")
        await ctx.reply(embed=errorEmbed)
    try:
        await bot.unload_extension("cogs."+arg)
        successEmbed = discord.Embed(color=green)
        successEmbed.add_field(name=f":white_check_mark: {arg} Cog disabled!", value="Hold tight while we conduct maintenance")
        await ctx.reply(embed=successEmbed)
    except:
        errorEmbed = discord.Embed(color=red)
        errorEmbed.add_field(name=":x: That is not a valid Cog!",value="(use $cogs to view them all)")
        await ctx.reply(embed=errorEmbed)

@bot.command(name="cogs", hidden=True)
@commands.has_permissions(administrator = True)
async def cogs(ctx):
    value = ""
    for ext in initial_extensions:
        name = str(ext).replace("cogs.","")
        value += name+'\n'
    cogEmbed = discord.Embed(color=defaultEmbedColor)
    cogEmbed.add_field(name="List of Cogs:", value=value)
    await ctx.reply(embed=cogEmbed)

###########################################################

async def loadall():
    for ext in initial_extensions:
        await bot.load_extension(ext)


async def gm(): # 09:00
    channel=bot.get_channel(588386911677186049)
    Guild = bot.get_guild(588386910951702550)
    file = open('./files/birthdays.json')
    data = json.load(file)
    bdays = []
    for thing in data:
        entry = str(data[thing])
        bday = entry.replace("[","").replace("]","").replace("'","")
        if date == bday:
            bdays.append(thing)
    if weekday == 4:
        gm = bot.get_cog("gm")
        await gm.sendgm(channel)
        return
    if len(bdays) > 0:
        for person in bdays:
            user = Guild.get_member(int(person))
            bdayEmbed = discord.Embed(color=defaultEmbedColor,description=":tada: *We got a birthday today!* :tada:")
            bdayEmbed.add_field(name="**Make sure to wish a happy birthday to** ", value = f"{user.mention}!")
            bdayEmbed.set_footer(text="I'm sure they'd appreciate it :)")
            bdayEmbed.set_thumbnail(url=user.display_avatar.url)
            await channel.send(embed=bdayEmbed)
    else:
        gmEmbed = discord.Embed(color=defaultEmbedColor, description="**Good Morning everyone! I hope you all have a great day!**")
        await channel.send(embed=gmEmbed)
        
async def dmt(): #22:00
        dm = bot.get_cog("dm")
        print("Created DM, sending")
        await dm.dm_tim()
       
async def cycleStatus(): #every hour      
        themes = bot.get_cog("ThemesCog")
        await themes.changeStatus()

schedule.every().hour.do(cycleStatus)
schedule.every().day.at("09:25").do(gm)
schedule.every().day.at("22:00").do(dmt)

async def runSchedule(): 
    while True:
        schedule.run_pending()
        time.sleep(1)

bot.remove_command('help')
asyncio.run(loadall())

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    print("Discord.py Version: "+discord.__version__)
    await runSchedule()

bot.run(os.getenv("DPY_key"))
