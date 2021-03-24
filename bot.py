import os
import discord
import asyncio
from discord import Template
import youtube_dl
from discord.voice_client import VoiceClient
from config import config
from utils.mongo import Document
import motor.motor_asyncio
from discord.ext import commands
import googletrans
from googletrans import Translator
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


bot = commands.Bot(command_prefix = commands.when_mentioned_or("s.", "strannik.", "/"), intents = discord.Intents.all())
bot.remove_command('help')
queue = []

#@bot.event
#async def on_error(err, *args, **kwargs):
#    raise

#@bot.event
#async def on_command_error(ctx, exc):
#    raise getattr(exc, "original", exc)

#queue = []

#@bot.command()
#async def translate(ctx, test: str, *, txt: str):
#    try:
#        t  = Translator()
#        result = t.translate(txt, dest=test)

        #embed = discord.Embed(title = f'**Перевод твоего сообщения**',
        #                  description = f"**Твое сообщение:** - {result.origin}\n\n"
        #                              f"**Перевод:** - {result.text}\n\n",
        #                 color = 0x00FF00)
        #embed.set_footer(text = f'{bot.user.name} © 2020 | Все права защищены', icon_url = bot.user.avatar_url)
        #embed.set_thumbnail(
        #    url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Google_Translate_logo_%28old%29.png')
    
        #await ctx.send(embed = embed)

    #except ValueError:
        #embed = discord.Embed(
        #    description = f':x: {ctx.author.mention}, данного **языка** не существует, я отправлю список **языков** тебе в **лс** :x:',
        #     color = 0xff0000)

        #embed.set_author(icon_url='https://www.flaticon.com/premium-icon/icons/svg/1828/1828665.svg',
        #                 name = 'Перевод | Ошибка')
        #embed.set_footer(text = f'{bot.user.name} © 2020 | Все права защищены', icon_url = bot.user.avatar_url)

        #await ctx.send(embed = embed)

        #languages = ", ".join(googletrans.LANGUAGES)

        #embed = discord.Embed(description = f'**Список всех языков:** {languages}',
        #                      color = 0x00FF00)

        #embed.set_footer(text = f'{bot.user.name} © 2020 | Все права защищены', icon_url = bot.user.avatar_url)

        #await ctx.author.send(embed = embed)

@bot.command()
async def translate(ctx, lang_to, *args):
    import googletrans
    from google_trans_new import google_translator  

    if lang_to not in googletrans.LANGCODES:
        embed = discord.Embed(
            description = f':x: {ctx.author.mention}, данного **языка** не существует, я отправлю список **языков** тебе в **лс** :x:',
            color = 0xff0000)

        embed.set_author(icon_url='https://www.flaticon.com/premium-icon/icons/svg/1828/1828665.svg',
                        name = 'Перевод | Ошибка')
        embed.set_footer(text = f'{bot.user.name} © 2021 | Все права защищены', icon_url = bot.user.avatar_url)

        await ctx.send(embed = embed)

        languages = ", ".join(googletrans.LANGUAGES)

        embed = discord.Embed(description = f'**Список всех языков:** {languages}',
                                color = 0x00FF00)

        embed.set_footer(text = f'{bot.user.name} © 2021 | Все права защищены', icon_url = bot.user.avatar_url)

        await ctx.author.send(embed = embed)
    else:
        translator = google_translator()  
        result = translator.translate(" ".join(args),lang_tgt=lang_to)  

        embed = discord.Embed(title = '**Перевод твоего сообщения**',
                        description = f"**Твое сообщение:** - {' '.join(args)}\n\n**Перевод:** - {result}\n\n",
                        color = 0x00FF00)
        embed.set_footer(text = f'{bot.user.name} © 2021 | Все права защищены', icon_url = bot.user.avatar_url)
        embed.set_thumbnail(
            url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Google_Translate_logo_%28old%29.png')

        msg = await ctx.send(embed = embed)
        await msg.add_reaction("🗑️")
        reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
        if str(reaction.emoji) == "🗑️":
            #idea_channel = self.bot.get_channel()
            await msg.clear_reactions()
            await ctx.message.delete()
        else:
            return False


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

    msg = await ctx.send('**Сейчас играет:** {}'.format(player.title))
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False
    del(queue[0])

@bot.command(name='queue', description='Добавление в список текстов')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    msg = await ctx.send(f'`{url}` Добавлено в список!')
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False

@bot.command(name='remove', description='Удаление песни в списке')
async def remove(ctx, number):
    global queue
    try:
        del(queue[int(number)])
        msg = await ctx.send(f'Теперь список: `{queue}!`')
        await msg.add_reaction("🗑️")
        reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
        if str(reaction.emoji) == "🗑️":
            #idea_channel = self.bot.get_channel()
            await msg.clear_reactions()
            await ctx.message.delete()
        else:
            return False
    
    except:
        msg = await ctx.send('Список пустой!')
        await msg.add_reaction("🗑️")
        reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
        if str(reaction.emoji) == "🗑️":
            #idea_channel = self.bot.get_channel()
            await msg.clear_reactions()
            await ctx.message.delete()
        else:
            return False

@bot.command(name='pause', description='Приостановить песню')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False

@bot.command(name='resume', description='Продолжение песни')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False

@bot.command(name='view', description='Просмотр песни')
async def view(ctx):
    msg = await ctx.send(f'Сейчас номер списка: `{queue}!`')
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False

@bot.command(name='leave', description='Выход бота из голосового канала')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False

@bot.command(name='stop', help='Остановить песню!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    msg = await ctx.reply("Успешно!")
    await msg.add_reaction("🗑️")
    reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
    if str(reaction.emoji) == "🗑️":
        #idea_channel = self.bot.get_channel()
        await msg.clear_reactions()
        await ctx.message.delete()
    else:
        return False

#@bot.command(description="Добавление песни в список:")
#async def queue_(ctx, url):
#    global queue

#    queue.append(url)
#    msg = await ctx.send(f'Песня: `{url}` успешно добавлена в список!')
#    msg.add_reaction("✅")

#@bot.command(description)

@bot.command()
async def unload(ctx, extins):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        bot.unload_extension(f'commands.{extins}')
        await ctx.send("OK!")
    else:
        return False

@bot.command()
async def load(ctx, extins):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        bot.load_extension(f'commands.{extins}')
        await ctx.send("OK!")
    else:
        return False

@bot.command()
async def reload(ctx, extins):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        bot.unload_extension(f'commands.{extins}')
        bot.load_extension(f'commands.{extins}')
        await ctx.send("OK!")
    else:
        return False

@bot.command()
async def user_back(ctx, member: discord.Member = None):
    def isnitro():
        if member.premium_since:
            return f'{member.premium_since.strftime("%d/%m/%Y")}'
        else:
            return 'Нету нитро'
    def isbot():
        if member.bot:
            return 'Да'
        else:
            return 'Нет'
    def isnick():
        if member.nick:
            return f'{member.nick}'
        else:
            return 'без изменений'
    def isactivity():
        desc = ""
        if not member.activity:
            desc += 'Нету статуса'
        else:
            current_activity = member.activities[0]
            if current_activity.type:        
                if current_activity.type == discord.ActivityType.playing:
                    desc += "Тип активности: Игра\n"
                    desc += f"Название: {current_activity.name}\n"
                    desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
                    #desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
                elif current_activity.type == discord.ActivityType.listening and not isinstance(current_activity, discord.Spotify):
                    desc += "Тип активности: Музыка\n"
                    desc += f"Слушает: {current_activity.name}\n"
                    desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}"
                    #desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}"
                elif current_activity.type == discord.ActivityType.listening and isinstance(current_activity, discord.Spotify):
                    desc += "Тип активности: Spotify\n"
                    desc += f"Название трека: {current_activity.title}\n"
                    desc += f"Название альбома: {current_activity.album}\n"
                    desc += f"Артисты: {', '.join(current_activity.artists)}\n"
                    total_seconds = current_activity.duration.seconds
                    hours = total_seconds // 3600
                    minutes = (total_seconds - hours * 3600) // 60
                    seconds = total_seconds - (hours * 3600 + minutes * 60)
                    desc += f"Продолжительность трека: {hours if str(hours) != '0' else '00'}:{minutes if str(minutes) != '0' else '00'}:{seconds if str(seconds) != '0' else '00'}\n"

                elif current_activity.type == discord.ActivityType.watching:
                    desc += "Тип активности: Просмотр\n"
                    desc += f"Смотрит: {current_activity.name}\n"
                    #desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}"
                    desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}"

                else:
                    desc += "Тип активности: Кастом\n"
                    desc += f"Играет в: {current_activity.name}\n"
                    desc += f"Создано: {current_activity.created_at.strftime('%d-%m-%Y %H:%M:%S')}"
        return desc
    if member is None:
        member = ctx.author
        embed = discord.Embed(title = f'Информация о {member.name}#{member.discriminator}', color = member.color)
        embed.add_field(name="ID Юзера:", value=member.id)
        embed.add_field(name="Ник на сервере:", value=isnick())
        embed.add_field(name="Дата получения нитро:", value=isnitro())
        embed.add_field(name="Присоеденился на сервер:", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Бот?", value=isbot())
        embed.add_field(name="roles", value=" ".join([role.mention for role in member.roles[1:]]))
        #embed.add_field(name="Роли:",value=" "role.mention for role in member.roles[1:]))

        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title = f'Информация о {member.name}#{member.discriminator}', color = member.color)
        embed.add_field(name="ID Юзера:", value=member.id)
        embed.add_field(name="Ник на сервере:", value=isnick())
        embed.add_field(name="Присоеденился на сервер:", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Бот?", value=isbot())
        embed.add_field(name="roles", value=f" ".join([role.mention for role in user.roles[1:]]))
        embed.add_field(name="Высшая роль:",value=member.top_role.mention)
        embed.add_field(name="Активность:", value=isactivity())
        embed.add_field(name="Дата получения нитро:", value=isnitro())
        await ctx.reply(embed=embed)

@bot.command()
async def u_test(ctx, user: discord.Member):

    embed = discord.Embed(title="Info:", description=f"Info of: {user.mention}", color=discord.Color.orange())

    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.connection_url = config["mongo_db"]
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["reaction_roles"]
    bot.reaction_roles = Document(bot.db, "react_r")
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