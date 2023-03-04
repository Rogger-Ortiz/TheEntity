import discord
from discord.ext import commands
import os
#Any extra libaries go under THIS LINE to import on live version
from musixmatch import Musixmatch

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
key = os.getenv('MUSIX_key')
musixmatch = Musixmatch(key)

class lyrics(commands.Cog):
    description="Wanna find out the lyrics of a song someone is listening to? Here's how!"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="lyrics", help="Search lyrics of what someone is listeng to!", usage="[user]")
    async def lyrics(self, ctx, user: discord.Member):
        activity = user.activity
        artist = activity.artists[0]
        track = activity.title
        results = musixmatch.track_search(q_track=track, q_artist=artist, page_size=1, page=1, s_track_rating='desc')
        track_id = results['message']['body']['track_list'][0]['track']['track_id']
        lyrics = musixmatch.track_lyrics_get(track_id)
        print(lyrics)
        return

async def setup(bot):
	await bot.add_cog(lyrics(bot))
