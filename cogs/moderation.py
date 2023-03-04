import discord
from discord.ext import commands
import pytesseract
import os
import json
import subprocess

pytesseract.pytesseract.tesseract_cmd=r'/usr/bin/tesseract'
defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

def scanAttachment(msg):
    # Grab image and run through pytesseract
    for image in msg.attachments:
        url = image.url
        print("Pytesseract will use: "+url)
        subprocess.run(["wget",url,"-O","checkImage.png"])
        imgSays = pytesseract.image_to_string('checkImage.png')
        print("Image Says: "+imgSays)
        os.remove("checkImage.png")
        return imgSays
    # Return what image says

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        file = open('/home/captain/boot/NTT/files/censor.json', 'r')
        data = json.load(file)
        partMatch = data['partMatch']
        fullMatch = data['fullMatch']
        full = str(msg.content)
        if msg.channel.guild == None:
            channel_name = "DM"
        else:
            channel_name = msg.channel.name
        if msg.attachments != []:
            print("Reading attachment... "+str(msg.attachments))
            caption = scanAttachment(msg)
            full += " " + str(caption).replace("\n", " ")
        print(f"({channel_name}) {msg.author.name}#{msg.author.discriminator}: {full}")
        sentence = str(full).split()
        if msg.channel.guild !=  None:
            for word1 in partMatch:
                for word2 in fullMatch:
                    if word1 in full or word2 in sentence:
                        word = "Attachment deleted."
                        if(word1 in msg.content):
                            word = word1
                        if(word2 in sentence):
                            word = word2
                        message = str(full)
                        author = str(msg.author.name)+"#"+str(msg.author.discriminator)
                        uid = msg.author.id
                        uav = msg.author.display_avatar.url
                        await msg.delete()
                        censorEmbed = discord.Embed(color=defaultEmbedColor, description=f"**Message sent by {msg.author.mention} deleted in {msg.channel.mention}**\n{message}")
                        censorEmbed.set_author(name=author, icon_url=uav)
                        censorEmbed.add_field(name="Reason",value="Banned Word",inline=True)
                        censorEmbed.add_field(name="Specifically:",value=word)
                        censorEmbed.set_footer(text="ID: "+str(uid))
                        channel=self.bot.get_channel(726204252992831521)
                        await channel.send(embed=censorEmbed)
                        return

async def setup(bot):
	await bot.add_cog(Moderation(bot))
