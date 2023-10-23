import discord
from discord.ext import commands

class EventsCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.Cog.listener()
    async def on_member_join(self, member):
        #Channels to send welcome
        cid = 1163897924577660978
        aid = 1163902606024900608
        channel = self.bot.get_channel(cid)
        channel2 = self.bot.get_channel(aid)
        #RJ user ID
        pid = 248440677350899712
        owner = self.bot.get_user(pid)
        
        #Get role to add to user
        role = "Unverified"
        await member.add_roles(discord.utils.get(channel.guild.roles, name=role))
        
        #Get rold to mention admins
        role2 = discord.utils.get(channel.guild.roles, name="Killers")

        #Welcome the user
        await channel.send(f"Welcome to The Campfire {member.mention}! Please wait for mods to verify your arrival. If you need any help, feel free to ask {owner.mention} or {role2.mention}!")
        
        #Alert mods to verify
        await channel2.send(f"User {member.mention} is awaiting verification {owner.mention}, {role2.mention}")


    @commands.has_any_role('Killers', 'The Observer')
    @commands.command(name="verify", help="Verifies a user for access to the server. (Admins only)", usage="$verify [user]")
    async def verify(self, ctx, member: discord.Member = None):
        if(ctx.channel.id != 1163897924577660978 ):
            await ctx.channel.send("Wrong channel")
            return
        aid = 1163902606024900608
        channel = self.bot.get_channel(aid)

        #Add Survivor Role
        await member.add_roles(discord.utils.get(channel.guild.roles, name="Survivors"))

        #Remove Unverified Role
        await member.remove_roles(discord.utils.get(channel.guild.roles, name="Unverified"))

        #Confirm verify
        await channel.send(f"User {member.mention} was verified by {ctx.author.mention}!")

async def setup(bot):
	await bot.add_cog(EventsCog(bot))
