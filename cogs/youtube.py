import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import time
import os
import asyncio
#Any extra libaries go under THIS LINE to import on live version

#import pynacl
from pytube import YouTube as YT

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
errEmbed = discord.Embed(color=defaultEmbedColor)
queue = []

def play_next(ctx):
    voice = ctx.message.guild.voice_client
    if len(queue) > 0:
        url = queue.pop(0)
        yt = YT(url)
        stream = yt.streams.get_by_itag(251)
        stream.download(output_path="/home/captain/boot/NTT/files/yt/",filename="audio.mp3")
        source = discord.FFmpegPCMAudio("/home/captain/boot/NTT/files/yt/audio.mp3")
        player = voice.play(source, after=lambda e: play_next(ctx))

class YouTube(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    
    @commands.command(name="play")
    async def play(self, ctx, url=None):
        if url==None or ("youtube.com" not in url and "youtu.be" not in url):
            await ctx.channel.send("Please enter a URL!")
            return
        
        try:
            queueEmbed = discord.Embed(color=defaultEmbedColor)
            voice = ctx.message.guild.voice_client
            if voice.is_playing():
                queue.append(url)
            queueEmbed.title="Video added to the queue!"
            queueEmbed.description="View using $queue"
            await ctx.send(embed=queueEmbed)
            return
        except:
            pass
        
        yt = YT(url)
        stream = yt.streams.get_by_itag(251)
        stream.download(output_path="/home/captain/boot/NTT/files/yt/",filename="audio.mp3")
        source = discord.FFmpegPCMAudio("/home/captain/boot/NTT/files/yt/audio.mp3")
        try:
            vc =  await ctx.author.voice.channel.connect()
        except:
            errEmbed.title="Not in a voice channel!"
            errEmbed.description="Please enter a voice channel before trying to play something!"
            await ctx.send(embed=errEmbed)
            return
        player = vc.play(source, after=lambda e: play_next(ctx))
        voice = ctx.message.guild.voice_client
        while voice.is_playing():
            await asyncio.sleep(30)
        await voice.disconnect(force=True)

    @commands.command(name="dc")
    async def dc(self, ctx):
        voice = ctx.message.guild.voice_client
        if voice.is_playing():
            voice.stop()
        await voice.disconnect(force=True)

    @commands.command(name="stop")
    async def stop(self, ctx):
        voice = ctx.message.guild.voice_client
        if not voice.is_playing:
            await ctx.send("Not playing anything!")
            return
        voice.stop()

    @commands.command(name="pause")
    async def pause(self, ctx):
        voice = ctx.message.guild.voice_client
        if not voice.is_playing():
            await ctx.send("Can't pause what is not playing!")
            return
        voice.pause()

    @commands.command(name="resume")
    async def resume(self, ctx):
        voice = ctx.message.guild.voice_client
        if not voice.is_paused():
            await ctx.send("Can't resume what is not paused!")
            return
        voice.resume()

    @commands.command(name="queue")
    async def queue(self, ctx):
        voice = ctx.message.guild.voice_client
        queueEmbed=discord.Embed(color=defaultEmbedColor)
        if len(queue) == 0:
            queueEmbed.title="No songs in queue!"
            queueEmbed.description="Add songs to the queue using $play!"
            await ctx.send(embed=queueEmbed)
            return
        counter = 1
        qString = ""
        for url in queue:
            yt = YT(url)
            qString+=f"{counter}. **{yt.author}**\n{yt.title}\n\n"
        queueEmbed.title="Queue:"
        queueEmbed.description=qString
        await ctx.send(embed=queueEmbed)

    @commands.command(name="remove")
    async def pop(self, ctx, num):
        popEmbed = discord.Embed(color=defaultEmbedColor)
        url = queue.pop(int(num)-1)
        title = YT(url).title
        author = YT(url).author
        popEmbed.title=f"Video removed from queue:"
        popEmbed.add_field(name=author, value=title)
        await ctx.send(embed=popEmbed)

    @commands.command(name="skip")
    async def skip(self, ctx):
        skipEmbed = discord.Embed(color=defaultEmbedColor)
        voice = ctx.message.guild.voice_client
        if not voice.is_playing():
            skipEmbed.title="Not playing anything!"
            await ctx.send(embed=skipEmbed)
            return
        voice.stop()
        play_next(ctx)



async def setup(bot):
	await bot.add_cog(YouTube(bot))
