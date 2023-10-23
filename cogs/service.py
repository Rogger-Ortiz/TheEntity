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
        embedMsg.add_field(name="TheCampfire.gg", value="A website for the server! In the future we plan on using the website to link modpacks, resources, and more! Visit here: **https://thecampfire.gg**", inline=True)
        embedMsg.add_field(name="Minecraft Server", value="A vanilla 1.20.2 Minecraft server! Join with IP: **mc.thecampfire.gg**", inline=True)
        embedMsg.add_field(name="Terraria Server", value="A brand new Terraria Server! Join using IP: **play.thecampfire.gg** and Port: **47272**", inline=True)
        embedMsg.add_field(name="Satisfactory Server", value="A Satisfactory server on the Rocky Desert! Join using IP: **play.thecampfire.gg** and Port: **57279**", inline=True)
        #embedMsg.add_field(name="", value="", inline=True)
        embedMsg.set_footer(text="Request what service you want to see!")
        await ctx.reply(embed=embedMsg)
    
async def setup(bot):
	await bot.add_cog(Service(bot))
