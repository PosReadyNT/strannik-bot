import discord
import time
import os
from discord import Activity, ActivityType
from discord.ext import commands, tasks

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Bot] - connected")
        servers = len(self.bot.guilds)
        global ia
        global ia2
        ia2 = 0
        ia = 0
        for filename in os.listdir('./events'):
            if filename.endswith('.py'):
                ia += 1
            if filename.endswith('.pyw'):
                os.system(f"rename {filename} {filename[:-1]}")
                ia += 1
        print(f"Loaded cogs events: {ia}")
        for filename2 in os.listdir('./commands'):
            if filename2.endswith('.py'):
                ia2 += 1
            if filename2.endswith('.pyw'):
                os.system(f"rename {filename2} {filename2[:-1]}")
                ia2 += 1
        print(f"Loaded cogs commands: {ia2}")

    @tasks.loop(seconds=15)
    async def change_stat():
        await self.bot.change_presence(status=discord.Status.idle,activity=Activity(name="s.help | strannikbot#3437", type=ActivityType.competing))
        time.sleep(15)
        await self.bot.change_presence(status=discord.Status.idle,activity=Activity(name=f"Я на {len(self.bot.guilds)} серверах", type=ActivityType.watching))
        time.sleep(15)

def setup(bot):
    bot.add_cog(Ready(bot))