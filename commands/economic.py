import discord, pymongo
from discord.ext import commands
from pymongo import MongoClient
from config import config
import random

class Economic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(config["mongo_db"])
        self.economic = self.clust["posready"]["economic"]
    
    @commands.command(aliases=["give-m", "money-give", "give"])
    async def give_money(self, ctx):
        money = random.randint(1, 1000)
        embed = discord.Embed(title="Деньги", description=f"Вы получили {money} денег!", color=discord.Color.orange())
        await ctx.send(embed=embed)
        a = self.economic.find_one({"_id": ctx.author.id})["money"]
        try:
            self.economic.update_one({"_id": ctx.author.id}, {"$set": {"money": a + money}})
        except:
            self.economic.delete_one({"_id": ctx.author.id})
            self.economic.insert_one({"_id": ctx.author.id, "money": a + money})

def setup(bot):
    bot.add_cog(Economic(bot))