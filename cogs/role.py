import discord
from discord.ext import commands
import json
import nest_asyncio

class Role(commands.Cog):
    description="Give yourself roles!"
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="role", help="Adds a role to the user", usage="[Role]")
    async def role(self, ctx, name=None):
        defaultEmbedColor=discord.Color(0xe67e22)
        green = discord.Color(0x00FF00)
        red = discord.Color(0xFF0000)

        file = open('/home/captain/boot/NTT/files/serverRoles.json', 'r')
        data = json.load(file)
        guildID = str(ctx.guild.id)
        role = str(name)
        roleEmbed = discord.Embed(color=defaultEmbedColor)
        successEmbed = discord.Embed(color=green)
        errorEmbed = discord.Embed(color=red)

        if name == None:
            try:
                list = data[guildID]
                roleList = ""
                for thing in list:
                    roleList += thing+"\n"
                roleEmbed.add_field(name="Available Roles to Add:", value=roleList, inline=False)
                roleEmbed.set_footer(text="Remember to use \"\" if a role is more than one word!!!")
                await ctx.send(embed=roleEmbed)
                return
            except KeyError:
                errorEmbed.add_field(name=":x: No roles created by me in this server!", value="Have an admin create one using $newrole [role]!")
                await ctx.send(embed=errorEmbed)
                return

        if role not in data[guildID]:
            errorEmbed.add_field(name=":x: \""+role+"\" doesn't exist!", value="View all roles using $role!")
            await ctx.send(embed=errorEmbed)
            return

        check = discord.utils.find(lambda r: r.name == role, ctx.channel.guild.roles)
        if check in ctx.author.roles:
            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name=role))
            successEmbed.add_field(name=":white_check_mark: Removed \""+role+"\" from your roles!", value="View all roles using $role!")
            await ctx.send(embed=successEmbed)
        else:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=role))
            successEmbed.add_field(name=":white_check_mark: Added \""+role+"\" to your roles!", value="View all roles using $role!")
            await ctx.send(embed=successEmbed)
        file.close()

    #######################################################################################################################################

    @commands.has_permissions(administrator=True)
    @commands.command(name="delrole", help="Deletes role from server", usage="[Index Num]", hidden=True)
    async def delrole(self, ctx, num=None):
        defaultEmbedColor=discord.Color(0xe67e22)
        green = discord.Color(0x00FF00)
        red = discord.Color(0xFF0000)

        file = open('./files/serverRoles.json', 'r+')
        data = json.load(file)
        guildID = str(ctx.guild.id)
        errorEmbed=discord.Embed(color=red)
        successEmbed=discord.Embed(color=green)
        roleEmbed=discord.Embed(title="Available Roles to Delete", color=defaultEmbedColor)
        roleEmbed.add_field(name="Syntax: $delrole [index_num]", value="Index number is the number above the corresponding role", inline=False)

        if num == None:
            try:
                list = data[guildID]
                count = 0
                for thing in list:
                    roleEmbed.add_field(name=count, value=thing, inline=True)
                    count = count+1
                await ctx.send(embed=roleEmbed)
                return
            except KeyError:
                errorEmbed.add_field(name=":x: No roles created by me in this server!", value="Create one using $newrole [role]!")
                await ctx.send(embed=errorEmbed)
                return

        try:
            index = int(num)
        except ValueError:
            errorEmbed.add_field(name=":x: Please input index number, not role name!", value="View index numbers using $delrole!")
            await ctx.send(embed=errorEmbed)
            return

        try:
            indexTest = data[guildID][index]
        except IndexError:
            errorEmbed.add_field(name=":x: No role with that index!", value="Please use $delrole to view all index values")
            await ctx.send(embed=errorEmbed)
            return

        if index >= 0:
            role = str(data[guildID][index])
            roleObj = discord.utils.get(ctx.guild.roles,name=data[guildID][index])
            await roleObj.delete()
            data[guildID].pop(index)
            file.truncate(0)
            file.seek(0)
            json.dump(data, file)
            successEmbed.add_field(name=":white_check_mark: Removed role \""+role+"\"!", value="view all roles using $role!")
            await ctx.send(embed=successEmbed)
        else:
            await ctx.send("No role with that number!")
            file.close()

	##############################################################################################################################################

    @commands.has_permissions(administrator=True)
    @commands.command(name="newrole", help="Adds new role to the server", usage="[Role Name] [Hex Color](optional)", hidden=True)
    async def newrole(self, ctx, name=None, color='0x95a5a6'):
        defaultEmbedColor=discord.Color(0xe67e22)
        green = discord.Color(0x00FF00)
        red = discord.Color(0xFF0000) 

        file = open('./files/serverRoles.json', 'r+')
        data = json.load(file)
        guildID = str(ctx.guild.id)
        role = str(name)
        errorEmbed = discord.Embed(color=red)
        successEmbed = discord.Embed(color=green)
        if '0x' not in color:
            errorEmbed.add_field(name=":x: Please enter a valid color Hex Value", value="For example: 0x95a5a6")
            await ctx.send(embed=errorEmbed)
            return

        if name==None:
            errorEmbed.add_field(name=":x: Please use correct syntax!",value="Syntax: $newrole [name] [hex color value](Optional)")
            await ctx.send(embed=errorEmbed)
            return

        try:
            if role not in data[guildID]:
                data[guildID].append(role)
            else:
                errorEmbed.add_field(name=":x: Role \""+role+"\" already exists!", value="View all roles using $role!")
                await ctx.send(embed=errorEmbed)
                return
            file.truncate(0)
            file.seek(0)
            json.dump(data, file)
        except KeyError:
            entry = f"{{\"{guildID}\": [\"{role}\"]}}"
            newEntry = json.loads(entry)
            data.update(newEntry)
            file.truncate(0)
            file.seek(0)
            json.dump(data, file)
        file.close()
        guild = ctx.guild
        await guild.create_role(name=role, color=discord.Color.from_str(color))
        successEmbed.add_field(name=":white_check_mark: Created role \""+role+"\"!", value="View all roles using $role!")
        await ctx.send(embed=successEmbed)

async def setup(bot):
	await bot.add_cog(Role(bot))
