import discord
import zipfile
import os
import re
import time
from pathlib import Path
from discord_slash import SlashCommand
from discord_slash import cog_ext
import aiofiles
import time

import requests
from discord.ext import commands
class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cwd = Path(__file__).parents[0]
        self.cwd = str(self.cwd)

    @commands.command()
    async def backup(self, ctx):
        if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
            import py7zr
            with py7zr.SevenZipFile('backup_bot.7z', 'w') as z:
                z.writeall(f'{self.cwd}')
            await ctx.author.send(file=discord.File(fp='backup_bot.7z', filename='backup_bot.7z'))
            os.system(f'cd {self.cwd}')
            os.system('D:')
            os.system("del backup_bot.7z")
        else:
            embed = discord.Embed(title="Backup messages")
            await ctx.reply("Вы не создатель бота!")

    @commands.command()
    async def upload(self, ctx):
        if ctx.author.id == 443484756613660674 or ctx.author.id == 694598900094599198:
            if ctx.message.attachments:
                if not ctx.message.attachments[0].filename.endswith(".zip"):
                    await ctx.message.delete()
                    await ctx.send("введите zip архив!")
                else:
                    with open(f'{self.cwd}/'+str(ctx.message.attachments[0].filename), 'wb') as f:
                        responce = requests.get(str(ctx.message.attachments[0].url))
                        f.write(responce.content)
                        await ctx.author.send(f"{ctx.message.attachments[0].filename} " + "ОК!")
                        await ctx.author.send(file=discord.File(fp=f'{self.cwd}/{ctx.message.attachments[0].filename}', filename=f'{ctx.message.attachments[0].filename}'))
                    await ctx.message.delete()
            else:
                await ctx.reply("error")
        else:
            await ctx.reply(f"{ctx.message.author.mention}, Вы не создатель!")

    @commands.command(name="history",description="Копирование истории и сохранение в txt файл")
    async def history(self, ctx, limited:int = None, channel: discord.TextChannel = None):
        times = time.time()
        if channel:
            f = await aiofiles.open("history.txt", 'w', encoding="utf-8")
            msg = await ctx.send(content="Ожидайте...")
            with open('history.txt', 'w', encoding="utf-8") as f:
                messages = await ctx.channel.history(limit=limited).flatten()
                messages.reverse()
                for messages in messages:
                    msg2 = await ctx.fetch_message(messages.id)
                    f.write(f"\ndate: {str(msg2.created_at.strftime('%d.%m.%y:%H:%M:%S'))}")
                    f.write(f"\nAuthor:{str(msg2.author.name)} : Content:\n{str(messages.content)}")
            await ctx.send(file=discord.File(fp=f'{self.cwd[:-8]}\\history.txt', filename='history.txt'))
            await ctx.send(content=f"Время выполнения ушло в: {times - time.time()}")
        else:
            await ctx.send(content="Введите id/упоминание канала!")

def setup(bot):
    bot.add_cog(Backup(bot))