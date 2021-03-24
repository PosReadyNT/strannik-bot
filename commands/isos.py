import discord
from mega import Mega
from discord.ext import commands

class Isos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Выбор скачивания архива из mega", usage="s.link <mega> <Leaked source <info on a command>>")
    async def link(self, ctx, *args):
        mega = Mega()
        m = bool(mega.login("artemblet535@gmail.com", "rwju2580@"))
        if m == True:
            print("OK")
        else:
            print("NOT OK")

def setup(bot):
    bot.add_cog(Isos(bot))