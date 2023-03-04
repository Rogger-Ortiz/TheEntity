import discord
from discord.ext import commands
import random

#Any extra libaries go under THIS LINE to import on live version


defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class dm(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    async def dm_tim(self):
        choice = random.randint(1,5)
        channel = await self.bot.get_user(118185757679550465).create_dm()
        message = ""
        match choice:
            case 1:
                message = "Good evening Tim, just a reminder to brush your teeth!"
            case 2:
                message = "Hey Tim! Just a friendly reminder to brush your teeth tonight."
            case 3:
                message = "Yo! Brush ya teeth, you'll thank yourself in 15 years when they arent falling out."
            case 4:
                message = "Time to brush those teeth! (If only they could do it themselves right?)"
            case 5:
                message = "Alright pause the game, we gotta make sure those teeth are brushed big guy"
        await channel.send(message)

async def setup(bot):
	await bot.add_cog(dm(bot))
