import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['h'], description="все команды", usage="<s.help>")
    async def help(self, ctx):
        prefix = "s."
        embed = discord.Embed(title = "Справка по командам", colour = discord.Colour.green())
        def isusage():
            if command.usage:
                return f'{command.usage}'
            else:
                return 'Использование команды стандартно.'
        def iscommanddescription():
            if command.description:
                return f'{command.description}'
            else:
                return 'Доп. информации об команде нету'
        for command in self.bot.commands:
            embed.add_field(name=f"{prefix}{command.name}", value=f"{iscommanddescription()}, {isusage()}", inline=True)
        embed.set_footer(text=f"©️ strannikbot все права защищены")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))