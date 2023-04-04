import discord
from discord.ext import commands

class EventsCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.Cog.listener()
    async def on_member_join(self, member):
        cid = 588386911677186049
        pid = 248440677350899712
        owner = self.bot.get_user(pid)
        channel = self.bot.get_channel(cid)
        role = "Survivors"
        await member.add_roles(discord.utils.get(channel.guild.roles, name=role))
        await channel.send(f"Welcome to The Campfire {member.mention}! If you need any help, feel free to ask {owner.mention}!")

async def setup(bot):
	await bot.add_cog(EventsCog(bot))
