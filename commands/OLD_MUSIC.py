import discord
from discord.ext import commands
import youtube_dl

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
def setup(bot):
    bot.add_cog(MusicCog(bot))