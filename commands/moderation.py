import discord
from discord.ext import commands
from pymongo import MongoClient
from config import config
from discord.utils import get

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(config["mongo_db"])
        self.durka = self.clust["posready"]["durka"]

    @commands.command(description="Настройка канал для дурки")
    async def durka_role(self, ctx, role: discord.Role = None):
        if not role:
            embed = discord.Embed(title="Ошибка", description="Введите id/упоменание роли для выдавания дурки! (если нет роли для дурки то создайте и настройте её для всех каналов\nкроме для специального дурки канала)", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            self.durka.insert_one({"_id": ctx.guild.id, "role": role.id})
            embed = discord.Embed(title="Успешно", description=f"Вы успешно записали роль {role.mention} в базу данных для дурки!", color=discord.Color.green())
            await ctx.send(embed=embed)
    
    @commands.command(description="Отправить пользователя в дурку")
    async def durka(self, ctx, member: discord.Member = None, *, reason = None):
        if not member:
            embed = discord.Embed(title="Ошибка", description="Введите пользователя! Пример: `s.durka <@user#1234>`", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif reason is None:
            embed = discord.Embed(title="Успешно", description=f"Пользователя {member.mention} дали дурку без причины!", color=discord.Color.green())
            await ctx.send(embed=embed)
            durka_role = discord.utils.get(member.guild.roles,id = self.durka.find_one({"_id":ctx.guild.id})["role"])
            await member.add_roles(durka_role)
        else:
            embed = discord.Embed(title="Успешно", description=f"Пользователя {member.mention} дали дурку по причине: {reason}!", color=discord.Color.green())
            await ctx.send(embed=embed)
            durka_role = discord.utils.get(member.guild.roles,id = self.durka.find_one({"_id":ctx.guild.id})["role"])
            await member.add_roles(durka_role)

    @commands.command(description="Убрать пользователя из дурки")
    async def rem_durka(self, ctx, member: discord.Member = None):
        if not member:
            embed = discord.Embed(title="Ошибка", description="Введите пользователя! Пример: `s.rem_durka <@user#1234>`", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Успешно", description=f"Пользователя {member.mention} дали дурку по причине: {reason}!", color=discord.Color.green())
            await ctx.send(embed=embed)
            durka_role = discord.utils.get(member.guild.roles,id = self.durka.find_one({"_id":ctx.guild.id})["role"])
            await member.remove_roles(durka_role)
            
    @commands.command(description="Бан участника", usage="s.ban <@user#1234> <причина>")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if not member:
            embed = discord.Embed(title="Ошибка", description="Введите пользователя!", colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        if member.id == ctx.author.id:
            embed = discord.Embed(title="Ошибка", description="Вы не можете забанить самого себя!",
                                  colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        if reason is None:
            embed = discord.Embed(title="Ошибка", description="Введите причину бана!",
                                  colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="Бан", description=f"Вас забанил {ctx.author.name} по причине:\n**{reason}**. "
                                                           f"Если это не так, то напишите администраторам или "
                                                           f"модераторам")
            embed.set_footer(text=f"{ctx.guild.id}")
            await member.send(embed=embed)
            await member.ban(reason=reason)


    @commands.command(description="Очистка чата", usage="<s.clear <число для очистки>>")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=arg)
        embed = discord.Embed(title="Очистка", description=f"Успешно я очистил {arg} сообщений(-е)",
                              colour=discord.Colour.green())
        await ctx.send(embed=embed, delete_after=6.5)


def setup(bot):
    bot.add_cog(Moderation(bot))
