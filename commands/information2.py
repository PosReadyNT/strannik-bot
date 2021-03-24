import json
from pymongo import MongoClient
import discord
from config import config as conf
from hurry.filesize import size
import platform
import requests
from discord.ext import commands
from Cybernator import Paginator

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Посмотреть аватарку пользователя или свою аватарку", usage="<Имя пользователя (не обязательно)>")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            embed = discord.Embed(title=f"Аватарка {member.name}", description=f"[ссылка на аватарку]({member.avatar_url})", color = member.color)
            embed.set_image(url=member.avatar_url)
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=f"Аватарка {member.name}", description=f"[ссылка на аватарку]({member.avatar_url})", color = member.color)
            embed.set_image(url=member.avatar_url)
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.reply(embed=embed)
    
    @commands.command(description="Информация о боте", usage="<s.about>")
    async def about(self, ctx):
        py = platform.python_version()
        dpy = discord.__version__
        servers = len(self.bot.guilds)
        guild = "Strannый городок"
        members = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title = 'О боте', description = f'Привет я Странник Бот, я создан для сервера **__{guild}__**. Я приватный-бот, но если уж хочешь пригласить на свой сервер, то вот [**ссылка**](https://discord.com/oauth2/authorize?client_id=814877333453799465&scope=bot&permissions=8) на приглашение', colour = discord.Colour.green())
        embed.add_field(name = 'Версия Python', value = f'{py}')
        embed.add_field(name = 'Версия discord.py', value = f'{dpy}')
        embed.add_field(name = 'Количество Серверов', value = f'{servers}')
        embed.add_field(name = 'Количество Участников', value = f'{members}')
        embed.set_footer(icon_url=self.bot.user.avatar_url, text='©️ strannikbot все права защищены')
        await ctx.send(embed=embed)

    @commands.command(aliases=["user", "u_i", "info", "юзер", "ю_и", "инфо"], description="Информация о пользователе или о себе", usage="<Имя пользователя (не обязательно)>")
    async def user_info(self, ctx, member: discord.Member = None):
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
            #elif member.activity.name:
            #    desc += f'{member.activity.name}'
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
            embed.add_field(name="Присоеденился на сервер:", value=member.joined_at.strftime("%d/%m/%Y"))
            embed.add_field(name="Бот?", value=isbot())
            embed.add_field(name="Роли", value=f" ".join([role.mention for role in member.roles[1:]]))
            embed.add_field(name="Высшая роль:",value=member.top_role.mention)
            embed.add_field(name="Активность:", value=isactivity())
            embed.add_field(name="Дата получения нитро:", value=isnitro())
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title = f'Информация о {member.name}#{member.discriminator}', color = member.color)
            embed.add_field(name="ID Юзера:", value=member.id)
            embed.add_field(name="Ник на сервере:", value=isnick())
            embed.add_field(name="Присоеденился на сервер:", value=member.joined_at.strftime("%d/%m/%Y"))
            embed.add_field(name="Бот?", value=isbot())
            embed.add_field(name="Роли:", value=f" ".join([role.mention for role in member.roles[1:]]))
            embed.add_field(name="Высшая роль:",value=member.top_role.mention)
            embed.add_field(name="Активность:", value=isactivity())
            embed.add_field(name="Дата получения нитро:", value=isnitro())
            await ctx.reply(embed=embed)

    @commands.command(aliases=["serverinfo", "infoserver", "серверинфо", "сервер", "инфосервер"], description="Информация о сервере", usage="<s.server>")
    async def server(self, ctx):
        def region(region:discord.VoiceRegion=None):
            if region==discord.VoiceRegion.amsterdam:
                return ":flag_nl: Амстердам"
            if region==discord.VoiceRegion.brazil:
                return ":flag_br: Бразилия"
            if region==discord.VoiceRegion.dubai:
                return ":flag_ae: Дубай"
            if region==discord.VoiceRegion.eu_central:
                return ":flag_eu: Центральная Европа"
            if region==discord.VoiceRegion.eu_west:
                return ":flag_eu: Западная Европа"
            if region==discord.VoiceRegion.europe:
                return ":flag_eu: Европа"
            if region==discord.VoiceRegion.frankfurt:
                return ":flag_fk: Франкфурт"
            if region==discord.VoiceRegion.hongkong:
                return ":flag_hk: Гонк-конг"
            if region==discord.VoiceRegion.india:
                return ":flag_in: Индия"
            if region==discord.VoiceRegion.japan:
                return ":flag_jp: Япония"
            if region==discord.VoiceRegion.london:
                return ":flag_gb: Лондон"
            if region==discord.VoiceRegion.russia:
                return ":flag_ru: Россия"
            if region==discord.VoiceRegion.singapore:
                return ":flag_sg: Сингапур"
            if region==discord.VoiceRegion.southafrica:
                return ":flag_af: Южная Африка"
            if region==discord.VoiceRegion.sydney:
                return ":flag_sy: Сидней"
            if region==discord.VoiceRegion.us_east:
                return ":flag_us: Востоковая Америка"
            if region==discord.VoiceRegion.us_south:
                return ":flag_us: Южная Америка"
            if region==discord.VoiceRegion.us_west:
                return ":flag_us: Западная Америка"
            if region==discord.VoiceRegion.vip_amsterdam:
                return "[VIP] :flag_nl: Амстердам"
            if region==discord.VoiceRegion.vip_us_east:
                return "[VIP] :flag_us: Востоковая Америка"
            if region==discord.VoiceRegion.vip_us_west:
                return "[VIP] :flag_us: Западная Америка"
            else:
                return '🏳️ Не знаю'
        def isafk():
            if ctx.guild.afk_channel:
                return f'{ctx.guild.afk_channel}'
            else:
                return 'Нету AFK канала'
        def isafktime():
            if ctx.guild.afk_timeout and ctx.guild.afk_channel:
                return f'{ctx.guild.afk_timeout}'
            else:
                return 'Нету'
        def isbanner():
            if ctx.guild.banner:
                return f'{ctx.guild.banner}'
            else:
                return 'Нету'
        def ismfa():
            if ctx.guild.mfa_level == 1:
                return '1 уровень'
            elif ctx.guild.mfa_level == 2:
                return '2 уровень'
            elif ctx.guild.mfa_level == 3:
                return '3 уровень'
            else:
                return 'Нету'
        def verify():
            if str(ctx.guild.verification_level) == "low":
                return 'Низкий'
            elif str(ctx.guild.verification_level) == "medium":
                return 'Средний'
            elif str(ctx.guild.verification_level) == "high":
                return 'Высокий'
            elif str(ctx.guild.verification_level) == "very_high":
                return 'Самый высокий'
            else:
                return 'Нету'
        def levelboost():
            if ctx.guild.premium_tier == 1:
                return '1 уровень'
            elif ctx.guild.premium_tier == 2:
                return '2 уровень'
            elif ctx.guild.premium_tier == 3:
                return '3 уровень'
            else:
                return '0 уровень'
        def isboost():
            if ctx.guild.premium_subscription_count:
                if ctx.guild.premium_subscription_count == 1:
                    return f'{ctx.guild.premium_subscription_count} буст'
                if ctx.guild.premium_subscription_count == 1 or ctx.guild.premium_subscription_count == 2 or ctx.guild.premium_subscription_count == 3 or ctx.guild.premium_subscription_count == 4:
                    return f'{ctx.guild.premium_subscription_count} буста'
                else:
                    return f'{ctx.guild.premium_subscription_count} бустов'
            else:
                return '0 бустов'
        def isvoice():
            if ctx.guild.voice_channels:
                return f'{len(ctx.guild.voice_channels)}'
            else:
                return '0'
        def issystemchannel():
            if ctx.guild.system_channel:
                return f'{ctx.guild.system_channel}'
            else:
                return 'Нету'
        def isrules():
            if ctx.guild.rules_channel:
                return f'{ctx.guild.rules_channel}'
            else:
                return 'Нету'

        def isiconanim():
            if ctx.guild.icon_url == ctx.guild.is_icon_animated:
                return 'Да'
            if ctx.guild.icon_url != ctx.guild.is_icon_animated:
                return 'Нет'

        embed1 = discord.Embed(title="Сервер инфо", colour=discord.Colour.green())
        embed1.add_field(name="Название сервера:",value=ctx.guild.name)
        embed1.add_field(name="Иконка сервера анимирована?",value=isiconanim())
        embed1.add_field(name="ID Сервера:", value=ctx.guild.id)
        embed1.add_field(name="Создатель:",value=ctx.guild.owner.mention)
        embed1.set_thumbnail(url=str(ctx.guild.icon_url))

        embed2 = discord.Embed(title="Сервер инфо", colour=discord.Colour.green())
        embed2.add_field(name="Количество эмодзи:",value=len(ctx.guild.emojis))
        embed2.add_field(name="Максимально слотов эмодзи:",value=ctx.guild.emoji_limit)
        embed2.add_field(name="Всего участников:",value=ctx.guild.member_count)
        embed2.add_field(name="Максимум мб для загрузки файлов:",value=size(ctx.guild.filesize_limit))
        embed2.add_field(name="АФК канал:",value=isafk())
        embed2.add_field(name="Таймаут АФК:", value=isafktime())
        embed2.add_field(name="Регион:", value=region(ctx.guild.region))
        embed2.set_thumbnail(url=str(ctx.guild.icon_url))

        embed3 = discord.Embed(title="Сервер инфо", colour=discord.Colour.green())
        embed3.add_field(name="Системный канал:", value=issystemchannel())
        embed3.add_field(name="Канал для правил:", value=isrules())
        embed3.add_field(name="Количество голосовых каналов",value=isvoice())
        embed3.add_field(name="Количество текстовых каналов:",value=len(ctx.guild.text_channels))
        embed3.add_field(name=f"Баннер:",value=isbanner())
        embed3.add_field(name=f"Уровень буста ({levelboost()}):",value=f"Количество бустов: {isboost()}")
        embed3.set_thumbnail(url=str(ctx.guild.icon_url))

        embed4 = discord.Embed(title="Сервер инфо", colour=discord.Colour.green())
        embed4.add_field(name="Уровень верификации модераторов:", value=ismfa())
        embed4.add_field(name="Уровень верификации:", value=verify())
        embed4.set_thumbnail(url=str(ctx.guild.icon_url))

        embed5 = discord.Embed(title="Сервер инфо")
        ret = requests.get('https://status.discordapp.com/index.json')
        rec = json.loads(ret.text)
        color = 0x000000
        if rec['status']['description'] == "Все системы в рабочем состоянии":
            color = 0x00D800
        else:
            color = 0xAA00AA
        embed5 = discord.Embed(title=rec['status']['description'],colour=color,description='Данные получены из [Discord\'s status](https://status.discordapp.com/index.json).')
        if rec["components"][0]["status"] == "operational":
            embed5.add_field(name="API",value="Отлично",inline=True)
        else:
            embed5.add_field(name="API",value='Не работает',inline=True)
        if rec["components"][1]["status"] == "operational":
            embed5.add_field(name="Шлюз",value='Отлично',inline=True)
        else:
            embed5.add_field(name="Шлюз",value='Не работает',inline=True)
        if rec["components"][2]["status"] == "operational":
            embed5.add_field(name="CloudFlare",value='Отлично',inline=True)
        else:
            embed5.add_field(name="CloudFlare",value='Не работает',inline=True)
        if rec["components"][3]["status"] == "operational":
            embed5.add_field(name="Медиа прокси",value='Отлично',inline=True)
        else:
            embed5.add_field(name="Шлюз",value='Не работает',inline=True)
        if rec["components"][3]["status"] == "operational":
            embed5.add_field(name="Голосовые серверы",value='Отлично',inline=True)
        else:
            embed5.add_field(name="Шлюз",value='Не работает',inline=True)
        embed5.set_thumbnail(url=str(ctx.guild.icon_url))

        embeds = [embed1, embed2, embed3, embed4, embed5]
        message = await ctx.send(embed=embed1)
        page = Paginator(self.bot, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()

def setup(bot):
    bot.add_cog(Information(bot))