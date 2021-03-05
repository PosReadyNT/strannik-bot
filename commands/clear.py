import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description="Очистка чата", usage="<s.clear <число для очистки>>")
    @commands.has_any_role('Moder', 'Админ')
    async def clear(self, ctx, arg:int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=arg)
        embed=discord.Embed(title="Очистка", description=f"Успешно я очистил {arg} сообщений(-е)", colour=discord.Colour.green())
        await ctx.send(embed=embed, delete_after=6.5)

def setup(bot):
    bot.add_cog(Clear(bot))