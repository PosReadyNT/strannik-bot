import os
import discord
import asyncio
import youtube_dl
from discord.voice_client import VoiceClient
from config import config
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions, errors

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
# ты тут? Я дал право писать. ну...
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1.0):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


bot = commands.Bot(command_prefix = commands.when_mentioned_or("s."), intents = discord.Intents.all())
bot.remove_command('help')
queue = []

#@bot.event
#async def on_error(err, *args, **kwargs):
#    raise

#@bot.event
#async def on_command_error(ctx, exc):
#    raise getattr(exc, "original", exc)

#queue = []

@bot.command(name='join', description="Вход бота в голосовой канал")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.reply("Вы не ввошли в голосовой!")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@bot.command(name='play', description='Воспроизвести песню')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Сейчас играет:** {}'.format(player.title))
    del(queue[0])

@bot.command(name='queue', description='Добавление в список текстов')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    msg = await ctx.send(f'`{url}` Добавлено в список!')
    await msg.add_reaction("✅")

@bot.command(name='remove', description='Удаление песни в списке')
async def remove(ctx, number):
    global queue
    try:
        del(queue[int(number)])
        msg = await ctx.send(f'Теперь список: `{queue}!`')
        await msg.add_reaction("✅")
    
    except:
        await ctx.send('Список пустой!')

@bot.command(name='pause', description='Приостановить песню')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("✅")

@bot.command(name='resume', description='Продолжение песни')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("✅")

@bot.command(name='view', description='Просмотр песни')
async def view(ctx):
    msg = await ctx.send(f'Сейчас номер списка: `{queue}!`')
    msg.add_reaction("✅")

@bot.command(name='leave', description='Выход бота из голосового канала')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("✅")

@bot.command(name='stop', help='Остановить песню!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("✅")

#@bot.command(description="Добавление песни в список:")
#async def queue_(ctx, url):
#    global queue

#    queue.append(url)
#    msg = await ctx.send(f'Песня: `{url}` успешно добавлена в список!')
#    msg.add_reaction("✅")

#@bot.command(description)


for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        bot.load_extension(f'events.{filename[:-3]}')
    if filename.endswith('.pyw'):
        os.system(f"rename {filename} {filename[:-1]}")
        bot.load_extension(f'events.{filename[:-3]}')

for filename2 in os.listdir('./commands'):
    if filename2.endswith('.py'):
        bot.load_extension(f'commands.{filename2[:-3]}')
    if filename2.endswith('.pyw'):
        os.system(f"rename {filename2} {filename2[:-1]}")
        bot.load_extension(f'commands.{filename2[:-3]}')

bot.run(config["token"])