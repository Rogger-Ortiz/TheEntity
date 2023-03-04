import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
from urllib.request import urlopen
from urllib.request import HTTPError
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
                      'cogs.events',
                      'cogs.qrcode',
                      'cogs.fun',
                      'cogs.moderation',
                      'cogs.vc',
                      'cogs.gifs',
                      'cogs.gm',
                      'cogs.dm',
                      'cogs.lyrics']


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


async def loadall():
    for ext in initial_extensions:
        await bot.load_extension(ext)

async def onboot(run): 
    while True:
        now = datetime.now()
        date = now.strftime("%m/%d")
        time = now.strftime("%H:%M%p")
        print(time)
        weekday = now.weekday()
        channel=bot.get_channel(588386911677186049)
        guildID = 588386910951702550
        Guild = bot.get_guild(guildID)

        if time == "09:00AM":
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
        if time == "22:00PM":
            dm = bot.get_cog("dm")
            print("Created DM, sending")
            await dm.dm_tim()
            print("Send!")
        if ":00" in time:
            themes = bot.get_cog("ThemesCog")
            await themes.changeStatus()

        await asyncio.sleep(60)


bot.remove_command('help')
asyncio.run(loadall())
@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    print("Discord.py Version: "+discord.__version__)
    boot_thread = Thread(target=onboot)
    if not boot_thread.is_alive():
        await onboot(1)
    else:
        print("Connection rebooted! Preventing second call for checking time...")

bot.run(os.getenv("DPY_key"))
