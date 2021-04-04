import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description="Бан участника", usage="s.ban <@user#1234> <причина>")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason):
        if not member:
            embed = discord.Embed(title="Ошибка", description="Введите пользователя!", colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        if member.id == ctx.author.id:
            embed = discord.Embed(title="Ошибка", description="Вы не можете забанить самого себя!", colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        if ctx.author.id < member.top_role:
            embed = discord.Embed(title="Ошибка", description="Вы не можете забанить самого себя!", colour=discord.Colour.red())
            await ctx.reply(embed=embed)

    @commands.command(description="Очистка чата", usage="<s.clear <число для очистки>>")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg:int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=arg)
        embed=discord.Embed(title="Очистка", description=f"Успешно я очистил {arg} сообщений(-е)", colour=discord.Colour.green())
        await ctx.send(embed=embed, delete_after=6.5)

def setup(bot):
    bot.add_cog(Moderation(bot))