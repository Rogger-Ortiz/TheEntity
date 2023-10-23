import discord
from discord.ext import commands, tasks
import datetime
import pytz
import json

#Any extra libaries go under THIS LINE to import on live version

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
est_raw = pytz.timezone('US/Eastern')

class Tasks(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot
        self.test.start()
        self.gm.start()
        self.dmt.start()
        self.cycleStatus.start()

    # Print code here
    testtime = datetime.time(hour=4, minute=20)

    @tasks.loop(time=testtime)
    async def test(self):
        print("I Work!")
        return

    gmtime = datetime.time(hour=13, minute=0)
    
    @tasks.loop(time=gmtime)
    async def gm(self): # 09:00
        channel= self.bot.get_channel(588386911677186049) # Live
        #channel= self.bot.get_channel(761019927170777108) # Test
        date = datetime.datetime.today().strftime('%m/%d')
        weekday = datetime.datetime.now().weekday()
        Guild = self.bot.get_guild(588386910951702550)
        file = open('/home/captain/boot/NTT/files/birthdays.json', 'r')
        data = json.load(file)
        bdays = []
        for thing in data:
            entry = str(data[thing])
            bday = entry.replace("[","").replace("]","").replace("'","")
            if date == bday:
                bdays.append(thing)
        if weekday == 4:
            gm = bot.get_cog("gm")
            await gm.sendgm(channel)
            return
        if len(bdays) > 0:
            for person in bdays:
                user = Guild.get_member(int(person))
                bdayEmbed = discord.Embed(color=defaultEmbedColor,description=":tada: *We got a birthday today!* :tada:")
                bdayEmbed.add_field(name="**Make sure to wish a happy birthday to** ", value = f"{user.mention}!")
                bdayEmbed.set_footer(text="I'm sure they'd appreciate it :)")
                bdayEmbed.set_thumbnail(url=user.display_avatar.url)
                await channel.send(embed=bdayEmbed)
        else:
            gmEmbed = discord.Embed(color=defaultEmbedColor, description="**Good Morning everyone! I hope you all have a great day!**")
            await channel.send(embed=gmEmbed)
        return
    
    timtime = datetime.time(hour=2, minute=0)
    
    @tasks.loop(time=timtime)
    async def dmt(self):#22:00
        return
        dm = self.bot.get_cog("dm")
        print("Created DM, sending")
        await dm.dm_tim()
        return
    
    @tasks.loop(hours=1)
    async def cycleStatus(self): #every hour      
        themes = self.bot.get_cog("ThemesCog")
        await themes.changeStatus()
        return

    @cycleStatus.before_loop
    async def beforeCycle(self):
        print('waiting...')
        await self.bot.wait_until_ready()

async def setup(bot):
	await bot.add_cog(Tasks(bot))
