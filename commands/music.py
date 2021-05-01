import asyncio
import discord
import itertools
import re
import sys
import traceback
import wavelink
from discord.ext import commands
from typing import Union

RURL = re.compile('https?:\/\/(?:www\.)?.+')


class MusicController:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.volume = 100
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = await self.queue.get()
            await player.play(song)
            self.now_playing = await self.channel.send(f'Сейчас играет: `{song}`')

            await self.next.wait()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        node = await self.bot.wavelink.initiate_node(host='localhost',
                                                     port=2333,
                                                     rest_uri='http://localhost:2333',
                                                     password='youshallnotpass',
                                                     identifier=f'{self.bot.user}',
                                                     region='us_central')

        node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    async def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('Музыкальные команды не могут быть в ЛС')
            except discord.HTTPException:
                pass

        print('Игнорирования команды {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='join', aliases=["j"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                return await ctx.send('Вы не в голосовом канале, войдите или напишите id голосового канала')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Вошёл в голосовой канал: **`{channel.name}`**', delete_after=15)
        await player.connect(channel.id)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query: str):
        if not RURL.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            return await ctx.send('Не найдено')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        track = tracks[0]

        controller = self.get_controller(ctx)
        await controller.queue.put(track)
        await ctx.send(f'`{str(track)}` добавлена в список', delete_after=15)

    @commands.command()
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Песня не может быть на паузе, т.к нету песни или песня уже на паузе',
                                  delete_after=15)

        await ctx.send('Песня на паузе', delete_after=15)
        await player.set_pause(True)

    @commands.command()
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.paused:
            return await ctx.send('Песня не может воспроизвести, т.к не было пауза', delete_after=15)

        await ctx.send('Воспроизведение песни...', delete_after=15)
        await player.set_pause(False)

    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Сейчас не играет никакая песня', delete_after=15)

        await ctx.send('Песня пропущена', delete_after=15)
        await player.stop()

    @commands.command()
    async def volume(self, ctx, *, vol: int = None):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("Вам нужно право на Администратора")
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not vol:
            return await ctx.send(f"Сейчас громкость: {controller.volume}")

        vol = max(min(vol, 100), 0)
        controller.volume = vol

        await ctx.send(f'Сейчас громкость: `{vol}`')
        await player.set_volume(vol)

    @commands.command(aliases=['np', 'current'])
    async def now_playing(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send('Сейчас не играет ничего')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(f'Сейчас играет: `{player.current}`')

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send('У вас нету списка с песнями', delete_after=20)

        upcoming = list(itertools.islice(controller.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{str(song)}`**' for song in upcoming)
        embed = discord.Embed(title=f'Всего количество песен: {len(upcoming)}', description="Песни:\n"+fmt)

        await ctx.send(embed=embed)

    @commands.command(aliases=['disconnect', 'dc'])
    async def leave(self, ctx):
        for vc in ctx.guild.voice_channels:
            members = [member.id for member in vc.members]
            if self.bot.user.id in members and ctx.author.id not in members:
                return await ctx.send("Бот не подключен до голосового канала")

        player = self.bot.wavelink.get_player(ctx.guild.id)

        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send('Бот не в голосовом')

        await player.disconnect()
        await ctx.send('Я отключился', delete_after=20)


def setup(bot):
    bot.add_cog(Music(bot))
