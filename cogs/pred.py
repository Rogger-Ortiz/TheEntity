import discord
from discord.ext import commands

#Any extra libaries go under THIS LINE to import on live version

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class Pred(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="pred", usage="[hero/item] [query]", help="Looks up a given hero or item in Predecessor!")
    async def pred(self, category, query):
        link = "https://omeda.city/"
        category = category.lower()
        match category:
            case "hero":
                link = link + "hero/"
            case "item":
                link = link + "item/"
        

async def setup(bot):
	await bot.add_cog(Pred(bot))
