import discord
from discord.ext import commands
from pymongo import MongoClient

class Msg_edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient("mongodb+srv://posready:rwju2580@starnnikcluster.btuqa.mongodb.net/posready?retryWrites=true&w=majority")
        self.dateb = self.clust.posready.data

def setup(bot):
    bot.add_cog(Msg_edit(bot))