import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class Service(commands.Cog):
    description="View Services using:"
    def __init__(self,bot):
        self.bot = bot

    # Print code here

    @commands.command(name="services", help="List all of the services I (RJ) run!", usage="")
    async def services(self, ctx):
        embedMsg = discord.Embed(title="Services", description="These are all of the services offered that are hosted by The Campfire!", color=defaultEmbedColor)
        embedMsg.add_field(name="The Entity Bot", value="Me! I am a continuously upgraded passion project maintained by RJ.\n(Github: **https://github.com/Rogger-Ortiz/TheEntity**)", inline=True)
        embedMsg.set_footer(text="More services to come in Summer 2023!")
        await ctx.reply(embed=embedMsg)
    
async def setup(bot):
	await bot.add_cog(Service(bot))
