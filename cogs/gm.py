import discord
from discord.ext import commands
import random

#Any extra libaries go under THIS LINE to import on live version

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class gm(commands.Cog):
    description="Testing to see if the commands under this perform as needed"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    async def sendgm(self, ctx):
        char = random.randint(1,5)
        match char:
            case 1:
                gmEmbed = discord.Embed(color=defaultEmbedColor, title="Good work Miners! You've made it to Friday. Management is very pleased with you all. Drinks are on them when you finish up.") 
                gmEmbed.set_image(url="https://steamuserimages-a.akamaihd.net/ugc/1861681734234511467/5C6B44C2498A33D6C2483A798115C42D29A41D36/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false")
            case 2:
                gmEmbed = discord.Embed(color=defaultEmbedColor, title="Another week well executed,\nTenno. I am pleased with your\nperformance. Finish today and we can\nsee what this weekend has in store.") 
                gmEmbed.set_image(url="https://static.wikia.nocookie.net/warframe/images/4/47/Lotus.png/revision/latest?cb=20200621132507&path-prefix=pl") 
            case 3:
                gmEmbed = discord.Embed(color=defaultEmbedColor, title="Way to go Superstar! You've made it to the end of the week. Just one more day and then you can enjoy your weekend.")
                gmEmbed.set_image(url="https://steamuserimages-a.akamaihd.net/ugc/1834652070002065886/1E06018B82782CEC10029C54EE473156BA879B0B/?imw=637&imh=358&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true")
            case 4:
                points = random.randint(5,10)
                points = f"{points} science collaboration points."
                users = ctx.guild.members
                user = random.choice(users)
                gmEmbed = discord.Embed(color=defaultEmbedColor, title=f"A rest? This is why **humans** are test subjects. Worthless time spent doing nothing. Testing resumes Monday.",description=f"**{user.mention} loses {points}**")
                gmEmbed.set_image(url="https://cdn.mos.cms.futurecdn.net/TFg2etQK9yjNqUrRwYHcDG.jpg")
            case 5:
                gmEmbed = discord.Embed(color=defaultEmbedColor, title="Happy Friday everyone! Is it just me, or did this week fly by? I know how hard all of you worked, so I hope you enjoy a well-deserved lovely weekend!")
                gmEmbed.set_image(url="https://cdn.mos.cms.futurecdn.net/iZikTSRa7VUU6FMKTkHfDf.jpg")
        await ctx.send(embed=gmEmbed)
        return

async def setup(bot):
	await bot.add_cog(gm(bot))
