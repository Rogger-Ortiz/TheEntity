import discord
from discord.ext import commands
import subprocess

#Any extra libaries go under THIS LINE to import on live version

class Length(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="length")
    async def length(self, ctx):
        size = subprocess.check_output(["/home/captain/boot/NTT/find.sh"])
        size = str(size)
        length = size.split("total")[0].split()[-1]
        print("Total = " + str(length))
        await ctx.send(str(length))


async def setup(bot):
	await bot.add_cog(Length(bot))
