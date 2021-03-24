import discord
from discord.ext import commands
import random
from config import config as conf
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime

class On_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(conf["mongo_db"])
        self.dateb=self.clust["posready"]["data"]
        self.member_join=self.clust["posready"]["member_join"]
        self.member_leave=self.clust["posready"]["member_leave"]
        self.bios=self.clust["posready"]["bio"]
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def join_member_channel(self, ctx, on=None, channel: discord.TextChannel=None):
        def colladd():
            post = {
                "_id": ctx.guild.id,
                "log": 0
            }
            self.member_join.insert_one(post)
        if on == "off":
            self.member_join.delete_one({"_id": ctx.guild.id})
            embed = discord.Embed(
                title = "Приветствие канал", 
                description = f"Канал для приветствия участника был отключен", 
                color = discord.Color.from_rgb(110, 196, 86)
            )
            msg = await ctx.reply(embed=embed)
            await msg.add_reaction('❌')
        else:
            if channel is None:
                await ctx.send(embed = discord.Embed(
                    description = f':x:{ctx.author.mention} укажите канал'))
            elif on == "on":
                colladd()
                self.member_join.update_one({"_id": ctx.guild.id}, {"$set": {"memberj_chan": channel.id}})
                    
                embed = discord.Embed(
                    title = "Приветствие канал", 
                    description = f"Канал для приветствия участника сервера был обновлён на: {channel.mention}", 
                    color = discord.Color.from_rgb(110, 196, 86))
                
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('✅')
                    

    @commands.command()
    #@commands.has_permissions(administrator=True)
    async def leave_member_channel(self, ctx, on=None, channel: discord.TextChannel=None):
        def colladd():
            post = {
                "_id": ctx.guild.id,
                "log": 0
            }
            self.member_leave.insert_one(post)
        if on == "off":
            self.member_leave.delete_one({"_id": ctx.guild.id})
            embed = discord.Embed(
                title = "Прощания канал", 
                description = f"Канал для прощания участника был отключен", 
                color = discord.Color.from_rgb(110, 196, 86)
            )
            msg = await ctx.reply(embed=embed)
            await msg.add_reaction('❌')
        else:
            if channel is None:
                await ctx.send(embed = discord.Embed(
                    description = f':x:{ctx.author.mention} укажите канал'))
            elif on == "on":
                colladd()
                self.member_leave.update_one({"_id": ctx.guild.id}, {"$set": {"memberl_chan": channel.id}})
                    
                embed = discord.Embed(
                    title = "Прощания канал", 
                    description = f"Канал для прощания участника сервера был обновлён на: {channel.mention}", 
                    color = discord.Color.from_rgb(110, 196, 86))
                
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('✅')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        idc = self.member_join.find_one({"_id": member.guild.id})["memberj_chan"]
        idc_text = self.member_join.find_one({"_id": member.guild.id})["text"]
        if idc == 0:
            return False
            self.bios.insert_one({"_id": ctx.author.id, "bio": 0})
        else:
            #if idc_text
            channel = self.bot.get_channel(idc)
            embed = discord.Embed(title='Новый участник',
                                description=f'Пользователь {member.mention} присоеденился к серверу!',
                                color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            await channel.send(embed=embed)
            self.bios.insert_one({"_id": ctx.author.id, "bio": 0})

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
        idc = self.member_leave.find_one({"_id": member.guild.id})["memberl_chan"]
        if idc == 0:
            return False
            self.bios.insert_one({"_id": ctx.author.id, "bio": 0})
        else:
            channel = self.bot.get_channel(idc)
            embed = discord.Embed(title='Выход участника',
                                  description=f'Пользователь {member.mention} вышёл из сервера. :(',
                                  color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            await channel.send(embed=embed)
            self.bios.insert_one({"_id": ctx.author.id, "bio": 0})

def setup(bot):
    bot.add_cog(On_member(bot))