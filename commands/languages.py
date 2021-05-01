import discord
from discord.ext import commands
from config import config
from pymongo import MongoClient


class Languages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(config["mongo_db"])
        self.langs = self.clust["posready"]["langs"]

    @commands.command()
    async def reg_lang(self, ctx):
        embed = discord.Embed(title="Enter the language",
                              description="Enter the language from reactions\n\n> 🇷🇺 - русский\n> 🇺🇸 - english")
        m = await ctx.send(embed=embed)
        await m.add_reaction("🇷🇺")
        await m.add_reaction("🇺🇸")
        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0,
                                                 check=lambda reaction, user: user.id == ctx.author.id and str(
                                                     reaction.emoji) in ["🇷🇺",
                                                                         "🇺🇸"] and reaction.message.id == m.id)
        if str(reaction.emoji) == "🇷🇺":
            await ctx.send("Перевод на русский")
            try:
                self.langs.insert_one({"_id": ctx.guild.id})
                self.langs.update_one({"_id": ctx.guild.id}, {"$set": {"lang": "ru"}})
            except:
                self.langs.delete_one({"_id": ctx.guild.id})
                self.langs.insert_one({"_id": ctx.guild.id})
                self.langs.update_one({"_id": ctx.guild.id}, {"$set": {"lang": "ru"}})
        elif str(reaction.emoji) == "🇺🇸":
            await ctx.send("translate from english")
            try:
                self.langs.insert_one({"_id": ctx.guild.id})
                self.langs.update_one({"_id": ctx.guild.id}, {"$set": {"lang": "en"}})
            except:
                self.langs.delete_one({"_id": ctx.guild.id})
                self.langs.insert_one({"_id": ctx.guild.id})
                self.langs.update_one({"_id": ctx.guild.id}, {"$set": {"lang": "en"}})

    @commands.command()
    async def testing_chan(self, ctx):
        if self.langs.find_one({"_id": ctx.guild.id})["lang"] == "ru":
            await ctx.send("Тест!")
        elif self.langs.find_one({"_id": ctx.guild.id})["lang"] == "en":
            await ctx.send("Test!")


def setup(bot):
    bot.add_cog(Languages(bot))
