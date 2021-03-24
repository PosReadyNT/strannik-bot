import discord
from googletrans import Translator
from discord.ext import commands

class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Translator(bot))