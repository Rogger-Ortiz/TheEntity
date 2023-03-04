import discord
from discord.ext import commands
import json
import nest_asyncio
import os
from riotwatcher import LolWatcher, ApiError

watcher = LolWatcher(os.getenv("RIOT_key"))
region = 'na1'

class Development(commands.Cog):
    description = "Developmental Commands (WIP):"

    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name='lol', help="Look up a league of legends user using their summoner name!", usage="[Summoner Name]")
    async def league(self, ctx, arg=None):
        if arg == None:
            helpEmbed = discord.Embed(color=0xFFA500, title="$lol [Summoner Name]")
            helpEmbed.add_field(name="[Summoner Name]", value="The display name inside of the League of Legends client. NOT to be confused with Riot ID")
            await ctx.send(embed=helpEmbed)
        else:
            try:
                summoner = str(arg)
                versions = watcher.data_dragon.versions_for_region(region)
                user = watcher.summoner.by_name(region, summoner)
                stats = watcher.league.by_summoner(region, user['id'])
                champs = watcher.champion_mastery.by_summoner(region, user['id'])
                print(user)
                #print(stats)
                #print(champs)

                embed = discord.Embed(color=0xFFD700, title = user['name'])
                icon_id = user['profileIconId']
                icon_version = versions['n']['profileicon']
                icon_url = "https://ddragon.leagueoflegends.com/cdn/"+str(icon_version)+"/img/profileicon/"+str(icon_id)+".png"
                embed.set_thumbnail(url=str(icon_url))
                embed.add_field(name="Level", value=user['summonerLevel'], inline=False)

                if(str(stats) != "[]"):
                    for ranked in stats:
                        match str(ranked['queueType']):
                            case 'RANKED_FLEX_SR':
                                type = "Ranked Flex"
                            case 'RANKED_SOLO_5x5':
                                type = "Ranked Solo"
                        embed.add_field(name=type, value=str(ranked['tier'])+" "+str(ranked['rank']), inline=True)
                await ctx.send(embed=embed)
            except ApiError as err:
                errorEmbed = discord.Embed(color=0xFF0000)
                if err.response.status_code == 404:
                    errorEmbed.add_field(name="<:missing:1040075742123409469> Summoner was not found!", value="Did someone ping missing?")
                    await ctx.send(embed=errorEmbed)

async def setup(bot):
	await bot.add_cog(Development(bot))
