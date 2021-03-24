import discord
from http.client import HTTPException
from discord.ext import commands

class Templates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.command()
    #async def temp(self, ctx):
    #    try:
    #        a = await ctx.guild.create_template(name=f'{ctx.guild.name}')
    #        await ctx.send(f"https://discord.new/{a.code}")
    #    except:
    #        await ctx.send("Уже есть код!")

def setup(bot):
    bot.add_cog(Templates(bot))