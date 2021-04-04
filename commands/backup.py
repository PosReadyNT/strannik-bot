import discord
import zipfile
import os
import re
import aiofiles
import time

import requests
from discord.ext import commands

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def backup(self, ctx):
        if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
            import py7zr
            with py7zr.SevenZipFile('backup_bot.7z', 'w') as z:
                z.writeall('D:/BACKUP/vashnoe/Projects Python/strannikbot')
            await ctx.author.send(file=discord.File(fp='backup_bot.7z', filename='backup_bot.7z'))
            os.system('cd D:/BACKUP/vashnoe/Projects Python/strannikbot/')
            os.system('D:')
            os.system("del backup_bot.7z")
        else:
            await ctx.reply("Вы не создатель бота!")

    @commands.command()
    async def upload(self, ctx):
        if ctx.author.id == 443484756613660674 or ctx.author.id == 694598900094599198:
            if ctx.message.attachments:
                if not ctx.message.attachments[0].filename.endswith(".zip"):
                    await ctx.message.delete()
                    await ctx.send("введите zip архив!")
                else:
                    with open('D:/BACKUP/vashnoe/Projects Python/strannikbot/'+str(ctx.message.attachments[0].filename), 'wb') as f:
                        responce = requests.get(str(ctx.message.attachments[0].url))
                        f.write(responce.content)
                        await ctx.author.send(f"{ctx.message.attachments[0].filename} " + "ОК!")
                        await ctx.author.send(file=discord.File(fp=f'D:/BACKUP/vashnoe/Projects Python/strannikbot/{ctx.message.attachments[0].filename}', filename=f'{ctx.message.attachments[0].filename}'))
                    await ctx.message.delete()
            else:
                await ctx.reply("error")
        else:
            await ctx.reply(f"{ctx.message.author.mention}, Вы не создатель!")

    @commands.command(description="Копирование истории и сохранение в txt файл",
                      usage="<s.history <ID канала (не обязательно)>>")
    async def history(self, ctx, channel: discord.TextChannel = None):
        def transform(message):
            return message.content

        if channel == None:
            channel = ctx.channel
            msg = await ctx.reply("Ожидайте...")

            #f = await aiofiles.open("history.txt", 'w', encoding="utf-8")

            with open('history.txt', 'w', encoding="utf-8") as f:
                messages = await ctx.channel.history(limit=None).flatten()
                messages.reverse()
                for message in messages:
                    msg2 = await ctx.fetch_message(message.id)
                    f.write('\ndate:' + msg2.created_at[:19])
                    f.write('\n' + str(msg2.author.name) + ':' + str(msg2.content))

            #messages = await ctx.channel.history(limit=None).flatten()
            #for i in messages:
            #    msg2 = await ctx.fetch_message(i.id)
            #    f.write('\ndate:'+str(i.created_at))
            #    f.write('\n'+str(i.author.name)+':'+str(i.content))
            #    await f.write(f'{i}\n')
            await msg.edit(content="Загрузка...")
            time.sleep(2)
            await msg.edit(content="Успешно!", delete_after=6)
            time.sleep(0.1)
            await ctx.author.send(file=discord.File(fp='D:/BACKUP/vashnoe/Projects Python/strannikbot/history.txt',
                                                    filename=f'channel.txt'))
        else:
            msg = await ctx.reply("Ожидайте...")
            messages_in_channel = await channel.history(limit=None).map(transform).flatten()

            f = await aiofiles.open("history.txt", 'w', encoding="utf-8")

            for i in messages_in_channel:
                await f.write(f'{i}\n')
            await msg.edit(content="Загрузка...")
            time.sleep(2)
            await msg.edit(content="Успешно!", delete_after=6)
            time.sleep(0.1)
            await ctx.author.send(file=discord.File(fp='D:/BACKUP/vashnoe/Projects Python/strannikbot/history.txt',
                                                    filename=f'channel.txt'))

def setup(bot):
    bot.add_cog(Backup(bot))