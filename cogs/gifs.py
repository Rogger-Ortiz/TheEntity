import discord
from discord.ext import commands
import os
import requests
import json
import random

#Any extra libaries go under THIS LINE to import on live version

class Gifs(commands.Cog):
    description="Search gifs using:"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="gif", help="Search Tenors gifs with a single command!", usage="[Gif name] [1-3](pick of top 3)")
    async def gif(self, ctx, arg=None, select=None):
        apikey = os.getenv("TENOR_key") # click to set to your apikey
        lmt = 3
        ckey = "the_entity_ckey"  # set the client_key for the integration and use the same value for all API calls

        # our test search
        search_term = str(arg)
        try:
            select = int(select)
        except:
            select = None

        # get the top 8 GIFs for the search term
        url = "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt)
        r = requests.get(url)
        print(url)
        if select == None:
            num = random.randint(1,lmt)
        else:
            if select > lmt:
                num = select%lmt
            else:
                num = select
        # load the GIFs using the urls for the smaller GIF sizes
        #try:
        gifs = json.loads(r.content)
        gifLink = gifs["results"][num-1]["media_formats"]["tinygif"]["url"]
        await ctx.send(gifLink)
        #except:
            #print("Error!")

async def setup(bot):
	await bot.add_cog(Gifs(bot))
