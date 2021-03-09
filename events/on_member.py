import discord
from discord.ext import commands
import random
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime

class On_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient("mongodb+srv://posready:rwju2580@starnnikcluster.btuqa.mongodb.net/posready?retryWrites=true&w=majority")
        self.dateb=self.clust["posready"]["member_join"]
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
            self.dateb.insert_one(post)
        if on == "off":
            if ctx.guild.id == 767096403549487124:
                self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"memberj_chan": 0}})
                embed = discord.Embed(
                    title = "Приветствие канал", 
                    description = f"Канал для приветствия участника был отключен", 
                    color = discord.Color.from_rgb(110, 196, 86)
                )
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('❌')
            else:
                self.dateb.delete_one({"_id": ctx.guild.id})
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
                if ctx.guild.id == 767096403549487124:
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"memberj_chan": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Приветствие канал", 
                        description = f"Канал для приветствия участника канал был обновлён на: {channel.mention}", 
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
                else:
                    colladd()
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"memberj_chan": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Приветствие канал", 
                        description = f"Канал для приветствия участника сервера был обновлён на: {channel.mention}", 
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def leave_member_channel(self, ctx, on=None, channel: discord.TextChannel=None):
        def colladd():
            post = {
                "_id": ctx.guild.id,
                "log": 0
            }
            self.dateb.insert_one(post)
        if on == "off":
            if ctx.guild.id == 767096403549487124:
                self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"memberl_chan": 0}})
                embed = discord.Embed(
                    title = "Прощания канал", 
                    description = f"Канал для прощания участника был отключен", 
                    color = discord.Color.from_rgb(110, 196, 86)
                )
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('❌')
            else:
                self.dateb.delete_one({"_id": ctx.guild.id})
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
                if ctx.guild.id == 767096403549487124:
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"memberl_chan": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Прощания канал", 
                        description = f"Канал для прощания участника канал был обновлён на: {channel.mention}", 
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
                else:
                    colladd()
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"memberl_chan": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Прощания канал", 
                        description = f"Канал для прощания участника сервера был обновлён на: {channel.mention}", 
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        idc = self.dateb.find_one({"_id": member.guild.id})["memberj_chan"]
        if idc == 0:
            return False
        else:
            channel = self.bot.get_channel(idc)
            embed = discord.Embed(title='Новый участник',
                                description=f'Пользователь {member.mention} присоеденился к серверу!',
                                color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
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
        idc = self.dateb.find_one({"_id": member.guild.id})["memberl_chan"]
        if idc == 0:
            idc = self.dateb.find_one({"_id": member.guild.id})["memberj_chan"]
            channel = self.bot.get_channel(idc)
            embed = discord.Embed(title='Выход участника',
                                  description=f'Пользователь {member.mention} вышёл из сервера. :(',
                                  color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            await channel.send(embed=embed)
        else:
            channel = self.bot.get_channel(idc)
            embed = discord.Embed(title='Выход участника',
                                  description=f'Пользователь {member.mention} вышёл из сервера. :(',
                                  color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(On_member(bot))