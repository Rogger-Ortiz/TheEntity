import discord
from discord.ext import commands
import openai
import os
import urllib.request
from urllib.request import urlopen
from urllib.request import HTTPError
import subprocess
from datetime import datetime
import threading
from threading import Thread
import asyncio

def getAvatarUrl(ctx):
	avatarUrl = ctx.author.guild_avatar
	if(avatarUrl == None):
		avatarUrl = ctx.author.avatar.url
	else:
		avatarUrl = ctx.author.guild_avatar.url
	return avatarUrl

def sanitize(msg):
    return msg.replace("@","@/")

defaultEmbedColor=discord.Color(0xe67e22)
openai.api_key = os.getenv("DALLE_key")
boostEmbed = discord.Embed(color=0xf47fff)
boostEmbed.add_field(name="<:boost:1040099133295444018> This command is for boosters only!", value="Your support would be much appreciated :)")
default = [{"role": "system", "content": "You are a friendly Discord bot named \"The Entity\" in a Discord server called \"The Campfire\". You assist the members in the server with questions they may have."}]
memory = []
memory.append(default[0])

class OpenAI(commands.Cog):
    description="Uses OpenAI to generate different media!"
    def __init__(self,bot):
        self.bot = bot

    # Print code here

    @commands.has_role('Offerings to The Entity')
    @commands.command(name="forget", help="Clears the AI's memory, to make room for a fresh set of queries", usage="")
    async def forget(self, ctx):
        global memory
        global default
        memory = []
        memory.append(default[0])
        wipeEmbed = discord.Embed(color=defaultEmbedColor)
        wipeEmbed.add_field(name="Memory wiped!", value="Ready for a new conversation!")
        await ctx.send(embed=wipeEmbed)

    @commands.command(name="history", help="Displays the bot's current memory in the form of \"User Input\" - Bot response", usage="")
    async def history(self, ctx):
        global memory
        global default
        print(memory)
        conversation = ""
        for item in memory:
            if item['role'] == 'system':
                continue
            if item['role'] == 'user':
                conversation = conversation + "\"" + item['content'] + "\"" + "\n\n"
            if item['role'] == 'assistant':
                conversation = conversation + " - " + item['content'] + "\n\n"
            if len(conversation) > 975:
                conversation = conversation[:975]
                conversation = conversation + "...\n\n**(Conversation truncated due to length)**"
                break
        convEmbed = discord.Embed(color=defaultEmbedColor)
        if len(conversation) < 1:
            convEmbed.add_field(name="No conversation yet!", value="Will you be the one to change that?")
        else:
            convEmbed.add_field(name="Most Recent Conversation:", value=conversation)
        await ctx.send(embed=convEmbed)

#######################################################################

    @commands.Cog.listener()
    async def on_message(self, msg):
        global memory
        global default
        if msg.author.bot:
            return
        if self.bot.user not in msg.mentions:
            return
#        if msg.author.premium_since == None and msg.author.id != 862548273951932416 and msg.author.id != 248440677350899712:
#            await msg.channel.send(embed=boostEmbed)
#            return
        if self.bot.user in msg.mentions:
            prompt = msg.content.split(self.bot.user.mention)
            inp = ""
            contentArr = []
            for seg in prompt:
                if len(seg) == 0:
                    continue
                inp = inp+seg
            contentArr.append({"type": "text", "text": inp})
            if len(msg.attachments) > 0:
                for att in msg.attachments:
                    contentArr.append({"type": "image_url", "image_url": att.url})
            memory.append({"role": "user", "content": contentArr})
            print(f"Checking memory...{len(memory)}")
            response = openai.ChatCompletion.create(
				#model="gpt-3.5-turbo",
                model="gpt-4",
				messages=memory
			)
            response = response['choices'][0]['message']['content']
            memory.append({"role": "assistant", "content": response})
            print(len(memory))
            if len(memory) > 11:
                memory = memory[2:]
                memory.append(default[0])
            parsedMsg = []
            parseStr = ""
            if len(response) > 6000:
                await msg.channel.send("I'm sorry, but my response is way too long for Discord to handle appropriately.")
                return
            if len(response) > 2000:
                for i in range(len(response)):
                    if i%1900 == 0:
                        parsedMsg.append(parseStr)
                        parseStr=""
                    parseStr += str(response[i])
                for string in parsedMsg:
                    await msg.channel.send(sanitize(string))
                return
            print(response)        
            await msg.channel.send(sanitize(response))
            return

###############################################################################################

    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.cooldown(1, 60, commands.BucketType.guild)
#    @commands.has_role('Offerings to The Entity')
    @commands.command(name="imagine", help="Generates an image based on user input!")
    async def imagine(self, ctx):
        errorEmbed = discord.Embed(color=0xFF0000)
        phrase = ctx.message.content[9:]
        if(phrase != None):
            await ctx.reply("Okay! Imagining " + phrase + ", give me a moment...")
            try:
                generation = openai.Image.create(
                    prompt = phrase,
                    n = 1,
                    size = "1024x1024"
                )
            except:
                errorEmbed.add_field(name=":x: Cannot Generate!", value="This could be because your request was NSFW or contained a persons face. Please do not request those. Your cooldown has been refunded.")
                await ctx.send(embed=errorEmbed)
                imagine.reset_cooldown(ctx)
                return
            print("Printing url...")
            image_url = generation['data'][0]['url']
            print(image_url)
            aiEmbed = discord.Embed(color=0x9fca53, title="Generated by: " + ctx.author.display_name)
            aiEmbed.set_thumbnail(url=getAvatarUrl(ctx))
            aiEmbed.add_field(name="Phrase:", value=phrase)
            print("Getting file")
            subprocess.run(["wget",image_url,"-O","image.jpg","-P","/home/captain/boot/NTT/cogs/"])
            print("File gotten")
            file = discord.File("./image.jpg", filename="image.jpg")
            aiEmbed.set_image(url="attachment://image.jpg")
            await ctx.send(file=file, embed=aiEmbed)
            os.remove("./image.jpg")
            if(ctx.author.id == 248440677350899712):
                imagine.reset_cooldown(ctx)
        else:
            helpEmbed = discord.Embed(color=0xFFA500)
            helpEmbed.add_field(name="$imagine [phrase]", value="Your phrase can be anything! Be as descriptive as you want!")
            await ctx.send(embed=helpEmbed)
            imagine.reset_cooldown(ctx)
    
    @imagine.error
    async def imagine_error(self, ctx, error):
        errorEmbed = discord.Embed(color=0xFF0000)
        if isinstance(error, commands.CommandOnCooldown):
            timeLeft = round(error.retry_after,2)
            errorEmbed.add_field(name=":x: Please wait 5 minutes before each request! ("+str(timeLeft)+"s left)", value="Thinking of these images takes a lot out of me...")
            await ctx.send(embed=errorEmbed)
        if isinstance(error, commands.MissingRole):
            await ctx.send(embed=boostEmbed)



async def setup(bot):
	await bot.add_cog(OpenAI(bot))
