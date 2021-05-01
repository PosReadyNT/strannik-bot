import discord
from discord.ext import commands


class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Изменить никнейм участника", usage="<s.nickname <Участник> <новый ник>>")
    @commands.has_permissions(manage_messages=True)
    async def nickname(self, ctx, member: discord.Member = None, *, nick: str = None):
        if member is None:
            embed = discord.Embed(title="Ошибка!", description="Введите участника!", colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        elif nick is None:
            embed = discord.Embed(title="Ошибка!", description="Введите ник!", colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        elif len(nick) > 32:
            embed = discord.Embed(title="Ошибка!", description="В дискорде ограничение ника до 32 символов!",
                                  colour=discord.Colour.red())
            await ctx.reply(embed=embed)
        else:
            def isnick():  # вот тут
                if member.nick:
                    return f'Изменился ник. Новый никнейм: `{member.nick}`'
                else:
                    return 'сбросился никнейм до стандартного'

            await member.edit(nick=nick)
            embed = discord.Embed(title="Успешно!", description=f"У {member.mention} {isnick()}",
                                  colour=discord.Colour.red())
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Nickname(bot))
