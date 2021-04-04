import discord
from pymongo import MongoClient
from config import config as conf
from discord.ext import commands
import datetime

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(conf["mongo_db"])
        self.dateb=self.clust["posready"]["data"]
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def logchannel(self, ctx, on=None, channel: discord.TextChannel=None):
        def colladd():
            post = {
                "_id": ctx.guild.id,
                "log": 0
            }
            self.dateb.insert_one(post)
        if on == "off":
            if ctx.guild.id == 767096403549487124:
                self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"log": 0}})
                embed = discord.Embed(
                    title = "Лог канал", 
                    description = f"Канал для логирования сервера был отключен", 
                    color = discord.Color.from_rgb(110, 196, 86)
                )
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('❌')
            else:
                self.dateb.delete_one({"_id": ctx.guild.id})
                embed = discord.Embed(
                    title = "Лог канал", 
                    description = f"Канал для логирования сервера был отключен", 
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
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"log": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Лог канал", 
                        description = f"Канал для логирования сервера был обновлён на: {channel.mention}\n\n Чтобы настроить логи введите команду: `s.log-s`",
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
                else:
                    colladd()
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"log": channel.id, "setting": 0}})
                        
                    embed = discord.Embed(
                        title = "Лог канал", 
                        description = f"Канал для логирования сервера был обновлён на: {channel.mention}\n\n Чтобы настроить логи введите команду: `s.log-s`",
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')

    @commands.command(aliases=["log_settings", "log_s", "log-s"], description="Настройка логов", usage="s.log_s")
    @commands.has_permissions(administrator=True)
    async def logs_settings(self, ctx):
        embed = discord.Embed(title="Настройка логов", description="Выберите реакцию:\n\n> 1️⃣ - включить все возможности лога\n> 2️⃣ - включить логи на удаление и изменения сообщения\n> 3️⃣ - включить логи на голосовые (переход/вход/выход)\n> 4️⃣ - включить логи на участника (Изменение аватарки/Изменение роли/Изменение ника)\n> 5️⃣ - включить логи на сервер (Создание/удаление каналов, ролей)", colour=discord.Colour.green())
        m = await ctx.send(embed=embed)
        await m.add_reaction("1️⃣")
        await m.add_reaction("2️⃣")
        await m.add_reaction("3️⃣")
        await m.add_reaction("4️⃣")
        await m.add_reaction("5️⃣")
        reaction, user = await self.bot.wait_for("reaction_add",timeout=60.0, check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"] and reaction.message.id == m.id)
        if str(reaction.emoji) == "1️⃣":
            self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"setting": 1}})
            await m.edit(content="Все настройки лога включены!")
        elif str(reaction.emoji) == "2️⃣":
            self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"setting": 2}})
            await m.edit(content="Настройка лога на удаление и изменения сообщения включено!")
        elif str(reaction.emoji) == "3️⃣":
            self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"setting": 3}})
            await m.edit(content="Настройка лога на голосовые включено!")
        elif str(reaction.emoji) == "4️⃣":
            self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"setting": 4}})
            await m.edit(content="Настройка лога на участника включено!")
        elif str(reaction.emoji) == "5️⃣":
            self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"setting": 5}})
            await m.edit(content="Настройка лога на сервер включено!")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        idc = self.dateb.find_one({"_id": before.guild.id}, {"log": before.channel.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.guild.id}, {"setting": 1 or 2})["setting"] == 1 or self.dateb.find_one({"_id": before.guild.id}, {"setting": 1 or 2})["setting"] == 2:
                if before.content != after.content:
                    channel_log = self.bot.get_channel(idc)
                    embed = discord.Embed(colour=discord.Colour.orange())
                    embed.set_author(name = f'Журнал аудита | Изменённое сообщение')
                    embed.add_field(name="Автор:", value=f"{before.author.name} ({before.author.id})")
                    embed.add_field(name="Канал:", value=f"<#{before.channel.id}>")
                    embed.add_field(name="Старое сообщение:", value=f"{before.content}")
                    embed.add_field(name="Изменёное сообщение:", value=f"{after.content}")
                    embed.set_footer(text=f"id сообщения: {before.id}")
                    await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        idc = self.dateb.find_one({"_id": message.guild.id}, {"log": message.channel.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": member.guild.id})["setting"] == 3 or self.dateb.find_one({"_id": member.guild.id})["setting"] == 4 or self.dateb.find_one({"_id": member.guild.id})["setting"] == 5:
                return False
            else:
                if message.content:
                    channel_log = self.bot.get_channel(idc)
                    embed = discord.Embed(colour=discord.Colour.orange())
                    embed.set_author(name = f'Журнал аудита | Удалённое сообщение')
                    embed.add_field(name="Автор:", value=f"{message.author.name} ({message.author.id})")
                    embed.add_field(name="Канал:", value=f"<#{message.channel.id}>")
                    embed.add_field(name="Удалённое сообщение:", value=f"{message.content}")
                    embed.set_footer(text=f"id сообщения: {message.id}")
                    await channel_log.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        idc = self.dateb.find_one({"_id": member.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": member.guild.id})["setting"] == 2 or self.dateb.find_one({"_id": member.guild.id})["setting"] == 4 or self.dateb.find_one({"_id": member.guild.id})["setting"] == 5:
                return False
            else:
                if after.channel == None:
                    if not before.channel == None:
                        if member.bot:
                            return
                        channel = self.bot.get_channel(idc) # Сюда свой канал логов
                        e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) вышел из голосового канала 🔊**', colour=discord.Colour.orange())
                        e.set_author(name = f'Журнал аудита | Выход из канала')
                        e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
                        e.add_field(name = "ID Участника", value = f"**{member.id}**")
                        return await channel.send(embed = e)

                if (not before.channel == None) and (not after.channel == None):
                    if before.channel.id == after.channel.id:
                        return

                    if member.bot:
                        return
                    channel = self.bot.get_channel(idc) # Сюда свой канал логов
                    e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) перешёл в другой голосовой канал 🔊**', colour=discord.Colour.orange())
                    e.set_author(name = f'Журнал аудита | Переход в канал')
                    e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
                    e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
                    e.add_field(name = "ID Участника", value = f"**{member.id}**")
                    return await channel.send(embed = e)

                if not after.channel == None:
                    if before.channel == None:
                        if member.bot:
                            return
                        channel = self.bot.get_channel(idc) # Сюда ид канала логов
                        e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) зашёл в голосовой канал 🔊**', colour=discord.Colour.orange())
                        e.set_author(name = f'Журнал аудита | Вход в канал')
                        e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
                        e.add_field(name = "ID Участника", value = f"**{member.id}**")
                        return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        idc = self.dateb.find_one({"_id": member.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.guild.id})["setting"] == 2 or self.dateb.find_one({"_id": before.guild.id})["setting"] == 3 or self.dateb.find_one({"_id": before.guild.id})["setting"] == 5:
                return False
            else:
                if before.avatar_url == after.avatar_url:
                    return
                else:
                    channel = self.bot.get_channel(idc) # Сюда ид канала логов
                    e = discord.Embed(description = f'**Пользователь {before.display_name}({before.mention}) изменил свой аватар!**', colour=discord.Colour.orange())
                    e.set_author(name = f'Журнал аудита | Измнение пользователя')
                    e.add_field(name = "Новая аватарка", value = f"**[Кликабельная ссылка]({before.avatar_url})**")
                    e.add_field(name = "ID Участника", value = f"**{before.id}**")
                    e.set_image(url = after.avatar_url)
                    return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        idc = self.dateb.find_one()["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one()["setting"] == 2 or self.dateb.find_one()["setting"] == 3 or self.dateb.find_one()["setting"] == 4:
                return False
            else:
                chanel = self.bot.get_channel(idc) # Сюда ид канала логов
                async for entry in chanel.guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_create):
                    if entry.user.bot:
                        return
                    else:
                        e = discord.Embed(colour=discord.Colour.orange())
                        e.set_author(name = 'Журнал аудита | Создание канала')
                        e.add_field(name = "Канал:", value = f"<#{entry.target.id}>")
                        e.add_field(name = "ID Канала:", value = f"{entry.target.id}")
                        e.add_field(name = "Создал:", value = f"{entry.user.mention} ({entry.user.id})")
                        await chanel.send(embed = e)
                        return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        idc = self.dateb.find_one()["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one()["setting"] == 2 or self.dateb.find_one()["setting"] == 3 or self.dateb.find_one()["setting"] == 4:
                return False
            else:
                chanel = self.bot.get_channel(idc) # Сюда ид канала логов
                async for entry in chanel.guild.audit_logs(action = discord.AuditLogAction.channel_delete):
                    if entry.user.bot:
                        return
                    else:
                        e = discord.Embed(colour=discord.Colour.orange())
                        e.set_author(name = 'Журнал аудита | Удаление канала')
                        e.add_field(name = "Канал:", value = f"{channel.name}")
                        e.add_field(name = "ID Канала:", value = f"{entry.target.id}")
                        e.add_field(name = "Удалил:", value = f"{entry.user.mention} ({entry.user.id})")
                        return await chanel.send(embed = e)
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        idc = self.dateb.find_one()["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one()["setting"] == 2 or self.dateb.find_one()["setting"] == 3 or self.dateb.find_one()["setting"] == 4:
                return False
            else:
                chanel = self.bot.get_channel(idc) # Сюда ид канала логов
                async for entry in chanel.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_create):
                    e = discord.Embed(colour=discord.Colour.orange())
                    e.set_author(name = 'Журнал аудита | Создание роли')
                    e.add_field(name = "Роль:", value = f"<@&{entry.target.id}>")
                    e.add_field(name = "ID роли:", value = f"{entry.target.id}")
                    e.add_field(name = "Создал:", value = f"{entry.user.mention} ({entry.user.id})")
                    await chanel.send(embed = e)
                    return
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        idc = self.dateb.find_one()["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one()["setting"] == 2 or self.dateb.find_one()["setting"] == 3 or self.dateb.find_one()["setting"] == 4:
                return False
            else:               
                chanel = self.bot.get_channel(idc) # Сюда ид канала логов
                async for entry in chanel.guild.audit_logs(action = discord.AuditLogAction.role_delete):
                    e = discord.Embed(colour=discord.Colour.orange())
                    e.set_author(name = 'Журнал аудита | Удаление роли')
                    e.add_field(name = "Роль:", value = f"{role.name}")
                    e.add_field(name = "ID роли:", value = f"{entry.target.id}")
                    e.add_field(name = "Удалил:", value = f"{entry.user.mention} ({entry.user.id})")
                    return await chanel.send(embed = e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        idc = self.dateb.find_one({"_id": before.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.guild.id})["setting"] == 2 or self.dateb.find_one({"_id": before.guild.id})["setting"] == 3 or self.dateb.find_one({"_id": before.guild.id})["setting"] == 5:
                return False
            else:
                if not len(before.roles) == len(after.roles):
                    role = [ ]
                    if len(before.roles) > len(after.roles):
                        for i in before.roles:
                            if not i in after.roles:
                                role.append(f'➖ Была убрана роль (<@&{i.id}>)\n')
                    elif len(before.roles) < len(after.roles):
                        for i in after.roles:
                            if not i in before.roles:
                                role.append(f'➕ Была добавлена роль (<@&{i.id}>)\n')
                    
                    str_a = ''.join(role)
                    channel = self.bot.get_channel(idc) # Сюда ид канала логов
                    e = discord.Embed(description = f'**У пользователя {after.display_name}({after.mention}) были изменены роли.**', colour=discord.Colour.orange())
                    e.set_author(name = f'Журнал аудита | Изменение ролей участника')
                    e.add_field(name = "Было сделано", value = f"**{str_a}**")
                    e.add_field(name = "ID Участника", value = f"**{after.id}**")
                    return await channel.send(embed = e)

                if not before.display_name == after.display_name:
                    channel = self.bot.get_channel(idc) # Сюда ид канала логов
                    e = discord.Embed(description = f'**Пользователь {before.display_name}({after.mention}) изменил NickName**', colour=discord.Colour.orange())
                    e.set_author(name = f'Журнал аудита | Изменение NickName участника')
                    e.add_field(name = "Действующее имя", value = f"**{after.mention}**")
                    e.add_field(name = "Предыдущее имя", value = f"**{before.display_name}**")
                    e.add_field(name = "ID Участника", value = f"**{after.id}**")
                    await channel.send(embed = e)

def setup(bot):
    bot.add_cog(Logs(bot))