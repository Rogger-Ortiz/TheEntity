import discord
from discord.ext import commands
import json

#Any extra libaries go under THIS LINE to import on live version

class VoiceChannel(commands.Cog):
    description="Customize your custom VC name using:"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            if after.channel.id == 1052076946210697256:
                category = after.channel.category
                memID = member.id
                file = open('/home/captain/boot/NTT/files/vcname.json', 'r+')
                data = json.load(file)
                guild = after.channel.guild
                
                channels = data["Channels"]
                try:
                    vcname = channels[str(memID)]
                except KeyError:
                    vcname = str(member.display_name)+"'s Channel"

                active = data["Active"]
                try:
                    channelID = (active[str(memID)])
                    existing = guild.get_channel(channelID)
                    await member.move_to(existing)
                    return
                except KeyError:
                    new_channel = await guild.create_voice_channel(vcname[0], category=category)
                    entry = f"{{\"{memID}\": [{new_channel.id}]}}"
                    newEntry = json.loads(entry)
                    active.update(newEntry)
                    #data.update(active)
                    file.truncate(0)
                    file.seek(0)
                    json.dump(data, file)
                    await member.move_to(new_channel)
                    file.close()
                    return
                
        if before.channel is not None:
            if before.channel.members == [] and before.channel.id != 1052076946210697256: 
                file = open('/home/captain/boot/NTT/files/vcname.json', 'r+')
                data = json.load(file)
                active = data["Active"]
                for channel in active:
                    if int(active[channel][0]) == before.channel.id:
                        active.pop(channel)
                        data.update(active)
                        file.truncate(0)
                        file.seek(0)
                        json.dump(data, file)
                        await before.channel.delete()
                        break
                file.close()
                return
    
    @commands.command(name="vcname", help=f"Renames your custom voice channel name!", usage="[Channel Name]")
    async def vcname(self, ctx):
        vcname = ctx.message.content[8:]
        vcname = vcname.replace("\"","")
        if vcname == None:
            ctx.send(":x: Please specify a name to track!")
            return

        defaultEmbedColor=discord.Color(0xe67e22)
        green = discord.Color(0x00FF00)
        red = discord.Color(0xFF0000)

        file = open('/home/captain/boot/NTT/files/vcname.json', 'r+')
        data = json.load(file)
        channels = data["Channels"]
        guildID = str(ctx.guild.id)
        memberID = str(ctx.author.id)
        Guild = self.bot.get_guild(int(guildID))

        vcname = str(vcname)
        errorEmbed = discord.Embed(color=red, description=":x: **An Error Occurred!**")
        successEmbed = discord.Embed(color=green, description=f":white_check_mark: **VC Name Successfully Changed to {vcname}!**")

        if memberID in channels:
            channels.pop(memberID)
        entry = f"{{\"{memberID}\": [\"{vcname}\"]}}"
        newEntry = json.loads(entry)
        print("New Entry: "+str(newEntry))
        channels.update(newEntry)
        file.truncate(0)
        file.seek(0)
        json.dump(data,file)
        await ctx.reply(embed=successEmbed)

async def setup(bot):
	await bot.add_cog(VoiceChannel(bot))
