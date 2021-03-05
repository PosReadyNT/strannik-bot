import discord
from discord.ext import commands
from discord.ext import *
import zipfile
import os

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['бэкап'])
    async def backup2(self, ctx):
        if ctx.author.id == 694598900094599198:
            await ctx.message.delete()
            with open('backup.txt', 'a') as f:
                messages = await ctx.channel.history(limit=None).flatten()
                for message in messages:
                    msg = await ctx.fetch_message(message.id)
                    f.write('\ndate:'+str(msg.created_at))
                    f.write('\n'+str(msg.author.name)+':'+str(msg.content))
            z = zipfile.ZipFile('backup.zip', 'w')
            for filename in os.listdir('./'):
                z.write(os.path.join('./', filename))
            for filename in os.listdir('./cogs'):
                z.write('./cogs/'+str(filename))
            z.close()
            await ctx.author.send(file=discord.File(fp='backup.zip', filename='backup.zip'))
            os.remove('backup.zip')

def setup(bot):
    bot.add_cog(Backup(bot))