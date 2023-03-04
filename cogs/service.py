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
        embedMsg.add_field(name="Tim and Trevor Modded Minecraft Server", value="A modded minecraft server that was made by our very own. Download the modpack here: https://drive.google.com/file/d/10yl5T825WH7CbYmDBwZIhWTiUvZKoYmF/view?usp=sharing\n(IP: **tnt.rjortiz.com**)", inline=True)
        embedMsg.add_field(name="Vanilla Minecraft Server", value="Just a plain old vanilla server, always updated to the latest version.\n(IP: **play.rjortiz.com**)", inline=True)
        embedMsg.add_field(name="The Entity Bot", value="Me! I am a continuously upgraded passion project maintained by RJ.\n**(Github: https://github.com/Rogger-Ortiz/TheEntity/blob/main/entity.py)**", inline=True)
        await ctx.reply(embed=embedMsg)
    
    @commands.command(name="reboot", hidden=True) 
    @commands.has_permissions(administrator = True)
    async def reboot(self, ctx, service):
        successEmbed = discord.Embed(color=0x00FF00)
        errorEmbed = discord.Embed(color=0xFF0000)
        match service:
            case "NTT":
                if(observer not in ctx.author.roles):
                    errorEmbed.add_field(name=":x: Only RJ can reboot me!", value="If you believe there is something wrong with me, please tell RJ, he will help from there.")
                    await ctx.reply(embed=errorEmbed)
                else:
                    successEmbed.add_field(name=":white_check_mark: As you wish.", value="Rebooting now.")
                    await ctx.reply(embed=successEmbed)
                    subprocess.run(['../reboot/sendCMD.sh', 'NTT'])
            case "TNT":
                successEmbed.add_field(name=":white_check_mark: The TNT Server will be restarted.", value="The server will be down momentarily, check back in a minute.")
                await ctx.reply(embed=successEmbed)
                subprocess.run(['../reboot/sendCMD.sh', 'TNT'])
            case "MMC":
                successEmbed.add_field(name=":white_check_mark: The MMC Server will be restarted.", value="The server will be down momentarily, check back in a minute")
                await ctx.reply(embed=successEmbed)
                subprocess.run(['../reboot/sendCMD.sh', 'MMC'])

async def setup(bot):
	await bot.add_cog(Service(bot))
