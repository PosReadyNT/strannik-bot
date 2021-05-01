import discord
from discord.ext import commands
from config import config
from pymongo import MongoClient
class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(config["mongo_db"])
        self.autoroles = self.clust["posready"]["autoroles"]
    
    @commands.command(name="autorole", description="Установить роль при входе участника")
    async def _autorole(self, ctx, role: discord.Role = None):
        if not role:
            embed = discord.Embed(title="Ошибка", description=f"Введите id/упоминание роли!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Успешно", description=f"Роль {role.mention} была успешно добавлена в базу данных!", color=discord.Color.green())
            await ctx.send(embed=embed)
            self.autoroles.insert_one({"_id": ctx.guild.id, "role": role.id})
    
    @commands.command(name="autorole_delete", description="Удаление автороли")
    async def _autorole_delete(self, ctx):
        try:
            embed = discord.Embed(title="Успешно", description=f"Автороль была успешно отключена в базе данных!", color=discord.Color.green())
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="Ошибка", description=f"Вы не регистрировали автороль при входе в боте либо случилась какая-то ошибка!", color=discord.Color.red())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Autoroles(bot))