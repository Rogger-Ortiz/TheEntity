import discord
from discord.ext import commands
import json
import nest_asyncio

class Birthday(commands.Cog):
    description="For tracking birthdays and displaying them too!"
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="birthday", help="Track your birthday and get a special embed when its your day!", usage="[mm/dd](optional)")
    async def birthday(self, ctx, bday=None):
        defaultEmbedColor=discord.Color(0xe67e22)
        green = discord.Color(0x00FF00)
        red = discord.Color(0xFF0000)

        file = open('/home/captain/boot/NTT/files/birthdays.json', 'r+')
        data = json.load(file)
        guildID = str(ctx.guild.id)
        memberID = str(ctx.author.id)
        Guild = self.bot.get_guild(int(guildID))
        if bday == None:
            listEmbed = discord.Embed(color=defaultEmbedColor)
            value = ""
            for memID in data:
                user = Guild.get_member(int(memID))
                string = str(user.display_name)+" - "+str(data[memID]).replace("[","").replace("]","").replace("'","")+"\n"
                value+=string
            listEmbed.add_field(name="Birthdays:", value=value)
            listEmbed.set_footer(text="Track your own birthday using \"$birthday [mm/dd]\"!")
            await ctx.reply(embed=listEmbed)
            return

        bday = str(bday)
        errorEmbed = discord.Embed(color=red, description=":x: **An Error Occurred!**")
        successEmbed = discord.Embed(color=green, description=":white_check_mark: **Birthday Successfully Tracked!**")

        if memberID in data:
            data.pop(memberID)
        entry = f"{{\"{memberID}\": [\"{bday}\"]}}"
        newEntry = json.loads(entry)
        data.update(newEntry)
        file.truncate(0)
        file.seek(0)
        json.dump(data,file)
        await ctx.reply(embed=successEmbed)

async def setup(bot):
	await bot.add_cog(Birthday(bot))
