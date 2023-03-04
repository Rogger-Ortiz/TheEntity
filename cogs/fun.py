import discord
from discord.ext import commands
import random
import time
import os
import subprocess

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class Fun(commands.Cog):
    description = "Miscellaneous Braindead Commands:"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="pfp", help="Displays a users current profile picture", usage="")
    async def pfp(self, ctx, member: discord.Member):
        pfpEmbed = discord.Embed(color = defaultEmbedColor)
        pfpLink = member.display_avatar.url
        pfpEmbed.set_author(name=member.display_name, icon_url=pfpLink)
        pfpEmbed.set_image(url=pfpLink)
        await ctx.reply(embed=pfpEmbed)

    @commands.command(name="poll", help="Creates a poll for users to react to", usage="\'[Question]\' [Answer 1] [Answer 2]")
    async def poll(self, ctx, ques=None, ans1=None, ans2=None):
        if ques == None or ans1 == None or ans2 == None:
            pollEmbed = discord.Embed(color=defaultEmbedColor, description="**:x: Please use $poll \"[Question]\" [Answer 1] [Answer 2]**")
            await ctx.reply(embed=pollEmbed)
            return
        question = ques
        answer1 = ans1
        answer2 = ans2
        name = ctx.author.name+"#"+ctx.author.discriminator
        icon = ctx.author.display_avatar.url

        pollEmbed = discord.Embed(color=defaultEmbedColor, description=f"**{question}**\n\n:one: {answer1}\n\n:two: {answer2}")
        pollEmbed.set_author(name=name, icon_url=icon)
        await ctx.message.delete()
        response = await ctx.send(embed=pollEmbed)
        await response.add_reaction('1️⃣')
        await response.add_reaction('2️⃣')

    @commands.command(name="length", help="Reads the length of the bots code!", usage="", hidden=True)
    async def length(self, ctx):
        size = subprocess.check_output(["/home/captain/boot/NTT/find.sh"])
        size = str(size)
        length = size.split("total")[0].split()[-1]
        print("Total = " + str(length))
        await ctx.send("The bot is "+str(length)+" lines long!")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="flip", help="Flips a coin, call it in the air!", usage="")
    async def flip(self, ctx):
        await ctx.send("Call it in the air!")
        HoT = random.randint(0,1)
        time.sleep(3.0)
        if(HoT):
            await ctx.send("It was Heads!")
        else:
            await ctx.send("It was Tails!")


    @commands.command(name="ryzeify", help="Turns all e's into Ryze's best combo, EQ", usage="")
    async def ryzeify(self, ctx, arg):
        ryzeEmbed = discord.Embed(color=0x737de7)
        if arg.find("e") != -1 or arg.find("E") != -1:
            txt = str(arg)
            reply = txt.replace("e", "e(Q)").replace("E", "E(Q)")
            ryzeEmbed.add_field(name="Ryze Says:", value=reply)
            ryzeEmbed.set_thumbnail(url="https://static.wikia.nocookie.net/leagueoflegends/images/2/23/Ryze_OriginalSquare.png/revision/latest/smart/width/250/height/250?cb=20160630224634")
            await ctx.reply(embed=ryzeEmbed)
        else:
            with open('./files/ThisGuyDoesntKnowHowToUseCommand.jpg', 'rb') as fp:
                await ctx.reply(file=discord.File(fp, 'ThisGuyDoesntKnowHowToUseCommand.jpg')) 
    
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="smash4", help="Don't show David this...", usage="")
    async def smash4(self, ctx):
        davidEmbed = discord.Embed(color=0xFC94AF)
        davidEmbed.set_thumbnail(url="https://media-exp1.licdn.com/dms/image/C4D03AQG0ek-qkG88jA/profile-displayphoto-shrink_200_200/0/1636168555634?e=2147483647&v=beta&t=_Md7pBD065Bb5IjSuEyRGbbCRizhuXxhlokqVTm36PM")
        davidEmbed.add_field(name="David Says:", value="Cool. I don’t care about being good at Smash 4 because that game was a pay to win shithole at its death and actually just worse than Brawl.")
        await ctx.send(embed=davidEmbed)
    
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="ballas", help="Don't worry, old friend. **I'm** not going to kill your boy...", usage="")
    async def ballas(self, ctx):
        ballasEmbed = discord.Embed(color=0xadd8e6)
        ballasEmbed.set_thumbnail(url="https://static.wikia.nocookie.net/warframe/images/5/5b/BallasPrologue.jpg/revision/latest?cb=20171223083810")
        with open('./files/ballas.ogg', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'ballas.ogg'))
        file=discord.File("./files/ballas.ogg", filename="ballas.ogg")
        ballasEmbed.set_image(url="attachment://ballas.ogg")
        ballasEmbed.add_field(name="Virtuvian Monologue", value="\"We had created monsters we couldn't control. We drugged them, tortured them, eviscerated them... we brutalized their minds, but it did not work. Until they came.\"\n\n\"And it was not their force of will, not their Void devilry, not their alien darkness... it was something else.\"\n\n\"It was that somehow, from within the derelict-horror, they had learned a way to see inside an ugly broken thing...\"\n\n\"...and take away its pain\"")
        await ctx.send(file=file, embed=ballasEmbed)
    
    @commands.command(name="305", help="Ese culo bota caca", usage="")
    async def threeohfive(self, ctx):
        await ctx.reply("https://i.imgur.com/2zos7RH.jpg")

async def setup(bot):
	await bot.add_cog(Fun(bot))
