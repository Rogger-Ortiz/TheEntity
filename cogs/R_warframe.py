import discord
from discord.ext import commands
import requests
import json

#Any extra libaries go under THIS LINE to import on live version

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class Warframe(commands.Cog):
    description="A way to look up events and items for Warframe (WIP)"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="wf")
    async def wf(self, ctx, arg):
        item = str(arg).lower()
        match arg:
            case "baro":
                c = requests.get("https://api.warframestat.us/pc/voidTrader/")
                data = c.json()
                wfEmbed = discord.Embed(color=0x774e37)
                if data["active"] == True:
                    wfEmbed.add_field(name="Baro Ki'Teer is currently at:", value=data["location"])
                    wfEmbed.set_thumbnail(url="https://static.wikia.nocookie.net/warframe/images/a/a7/TennoCon2020BaroCropped.png/revision/latest?cb=20200712232455")
                    inventory = data["inventory"]
                    inv = ""
                    for item in inventory:
                        item=str(item)+"\n"
                        inv+=item
                    wfEmbed.add_field(name="Baro is currently selling:", value=inv)
                    wfEmbed.add_field(name="Baro is leaving in:", value=data["endString"])
                    await ctx.reply(embed=wfEmbed)
                    return
                if data["active"] == False:
                    wfEmbed.set_image(url="https://static.wikia.nocookie.net/warframe/images/a/a7/TennoCon2020BaroCropped.png/revision/latest?cb=20200712232455")
                    wfEmbed.add_field(name="Baro Ki'Teer will arrive at:", value=data["location"]+" in "+data["startString"])
                    await ctx.reply(embed=wfEmbed)
                    return

async def setup(bot):
	await bot.add_cog(Warframe(bot))
