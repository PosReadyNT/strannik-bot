import discord
from discord.ext import commands
import random
from datetime import datetime

class On_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        self.bot.colors = {
            'WHITE': 0xFFFFFF,
            'AQUA': 0x1ABC9C,
            'GREEN': 0x2ECC71,
            'BLUE': 0x3498DB,
            'PURPLE': 0x9B59B6,
            'LUMINOUS_VIVID_PINK': 0xE91E63,
            'GOLD': 0xF1C40F,
            'ORANGE': 0xE67E22,
            'RED': 0xE74C3C,
            'NAVY': 0x34495E,
            'DARK_AQUA': 0x11806A,
            'DARK_GREEN': 0x1F8B4C,
            'DARK_BLUE': 0x206694,
            'DARK_PURPLE': 0x71368A,
            'DARK_VIVID_PINK': 0xAD1457,
            'DARK_GOLD': 0xC27C0E,
            'DARK_ORANGE': 0xA84300,
            'DARK_RED': 0x992D22,
            'DARK_NAVY': 0x2C3E50
        }
        self.bot.color_list = [c for c in self.bot.colors.values()]
        channel = discord.utils.get(member.guild.text_channels, name='приветствие')
        embed = discord.Embed(title='Новый участник',
                              description=f'Пользователь {member.mention} присоиденился к серверу! нас теперь {len(set(self.bot.get_all_members()))}!',
                              color=random.choice(self.bot.color_list))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        me = self.bot.get_user(694598900094599198)
        emb = discord.Embed(title=f'Уведомление', description='Бот пришел на новый сервер.',
                            color=0x00de68)  # Цвет - зеленый
        channel = guild.system_channel
        link = await channel.create_invite()
        emb.add_field(name=guild.name, value=f'Ссылка: {link}')
        emb.set_author(name=me, icon_url=me.avatar_url)
        emb.set_footer(text=f'{self.bot.user.name} © 2020 | Все права защищены', icon_url=self.bot.user.avatar_url)
        await me.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='приветствие')
        if channel:
            embed = discord.Embed(title='Выход участника',
                                  description=f'Пользователь {member.mention} вышёл из сервера. нас теперь {len(set(self.bot.get_all_members()))} :(',
                                  color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)

        else:
            return

def setup(bot):
    bot.add_cog(On_member(bot))