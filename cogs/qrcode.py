import discord
from discord.ext import commands
import os
import pyqrcode
import png
from pyqrcode import QRCode

class QRCode(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        raw = msg.content
        if "https://www.twitch.tv" in raw and msg.channel.id == 745774124806176799:
            startloc = raw.find("https://www.twitch.tv")
            url = raw[startloc:]
            url = url.split()[0]
            print("TWITCH URL: "+url)
            qrObj = pyqrcode.create(url)
            print("Obj Created")
            qrObj.png('qr.png', scale=6)
            print("Png downloaded")
            with open('/home/captain/boot/NTT/qr.png', 'rb') as qr:
                await msg.channel.send(file=discord.File(qr, "QRCode.png"))
                await msg.channel.send("...or use this qr code... if you're into that")
            os.remove('/home/captain/boot/NTT/qr.png')
async def setup(bot):
	await bot.add_cog(QRCode(bot))
