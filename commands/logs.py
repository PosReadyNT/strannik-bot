import discord
from pymongo import MongoClient
from config import config as conf
from discord.ext import commands
import io
import datetime
from time import sleep


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(conf["mongo_db"])
        self.dateb = self.clust["posready"]["data"]
        self.langs = self.clust["posready"]["langs"]
        self.mat = self.clust["posready"]["filter_mat"]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def logchannel(self, ctx, on=None, channel: discord.TextChannel = None):
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
                    title="Лог канал",
                    description=f"Канал для логирования сервера был отключен",
                    color=discord.Color.from_rgb(110, 196, 86)
                )
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('❌')
            else:
                self.dateb.delete_one({"_id": ctx.guild.id})
                embed = discord.Embed(
                    title="Лог канал",
                    description=f"Канал для логирования сервера был отключен",
                    color=discord.Color.from_rgb(110, 196, 86)
                )
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('❌')
        else:
            if channel is None:
                await ctx.send(embed=discord.Embed(
                    description=f':x:{ctx.author.mention} укажите канал'))
            elif on == "on":
                if ctx.guild.id == 767096403549487124:
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"log": channel.id}})

                    embed = discord.Embed(
                        title="Лог канал",
                        description=f"Канал для логирования сервера был обновлён на: {channel.mention}\n\n Чтобы "
                                    f"настроить логи введите команду: `s.log-s`",
                        color=discord.Color.from_rgb(110, 196, 86))

                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
                else:
                    colladd()
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"log": channel.id, "setting": 0}})

                    embed = discord.Embed(
                        title="Лог канал",
                        description=f"Канал для логирования сервера был обновлён на: {channel.mention}\n\n Чтобы "
                                    f"настроить логи введите команду: `s.log-s`",
                        color=discord.Color.from_rgb(110, 196, 86))

                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')

    @commands.command(aliases=["log_settings", "log_s", "log-s"], description="Настройка логов", usage="s.log_s")
    @commands.has_permissions(administrator=True)
    async def logs_settings(self, ctx):
        embed = discord.Embed(title="Настройка логов",
                              description="Выберите реакцию:\n\n> 1️⃣ - включить все возможности лога\n> 2️⃣ - "
                                          "включить логи на удаление и изменения сообщения\n> 3️⃣ - включить логи на "
                                          "голосовые (переход/вход/выход)\n> 4️⃣ - включить логи "
                                          "на сервер (Создание/удаление каналов, ролей)",
                              colour=discord.Colour.green())
        m = await ctx.send(embed=embed)
        await m.add_reaction("1️⃣")
        await m.add_reaction("2️⃣")
        await m.add_reaction("3️⃣")
        await m.add_reaction("4️⃣")
        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0,
                                                 check=lambda reaction, user: user.id == ctx.author.id and str(
                                                     reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"
                                                                        ] and reaction.message.id == m.id)
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
            self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"setting": 5}})
            await m.edit(content="Настройка лога на сервер включено!")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     filt = self.mat.find_one({"_id": message.guild.id})["mat"]
    #     msg = message.content.lower()
    #     if filt == 0:
    #         return False
    #     else:
    #         for filt_mat in filt:
    #             if filt_mat in message.content.lower():
    #                 await message.delete()
    #                 if self.langs.find_one({"_id": message.guild.id})["lang"] == "en":
    #                     m = await message.channel.send(embed = discord.Embed(
    #                         description = f':x: {message.author.mention}, Don`t say bad words!',
    #                         color = discord.Color.green()))
    #                     sleep(5)
    #                     await m.delete()
    #                 elif self.langs.find_one({"_id": message.guild.id})["lang"] == "ru":
    #                     m = await message.channel.send(embed = discord.Embed(
    #                         description = f':x: {message.author.mention}, не матерись!',
    #                         color = discord.Color.green()))
    #                     sleep(5)
    #                     await m.delete()
            # if msg in filt:
            #     await message.delete()
            #     if self.langs.find_one({"_id": message.guild.id})["lang"] == "en":
            #         await message.channel.send(embed = discord.Embed(
            #             description = f':x: {message.author.mention}, Don`t say bad words!',
            #             color = discord.Color.green()))
            #     elif self.langs.find_one({"_id": message.guild.id})["lang"] == "ru":
            #         await message.channel.send(embed = discord.Embed(
            #             description = f':x: {message.author.mention}, не матерись!',
            #             color = discord.Color.green()))
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        idc = self.dateb.find_one({"_id": before.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": before.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if before.name != after.name:
                    if self.langs.find_one({"_id": before.id})["lang"] == "en":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Journal Audit | new server name")
                        embed.add_field(name="Old server name:", value=before.name)
                        embed.add_field(name="New server name:", value=after.name)
                        embed.set_footer(text=f"server id: {after.id}")
                        await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": before.id})["lang"] == "ru":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Журнал Аудита | Новое название сервера")
                        embed.add_field(name="Старое название сервера:", value=before.name)
                        embed.add_field(name="Новое название сервера:", value=after.name)
                        embed.set_footer(text=f"id сервера: {after.id}")
                        await channel_log.send(embed=embed)
                if before.system_channel != after.system_channel and after.system_channel is not(None):
                    if self.langs.find_one({"_id": before.id})["lang"] == "en":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Journal Audit | new system channel")
                        embed.add_field(name="Old system channel:", value=before.system_channel)
                        embed.add_field(name="New system channel:", value=after.system_channel)
                        embed.set_footer(text=f"server id: {after.id}")
                        await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": before.id})["lang"] == "ru":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Журнал Аудита | Новый системный канал")
                        embed.add_field(name="Старый системный канал:", value=before.system_channel)
                        embed.add_field(name="Новый системный канал:", value=after.system_channel)
                        embed.set_footer(text=f"id сервера: {after.id}")
                        await channel_log.send(embed=embed)
                if before.rules_channel != after.rules_channel and after.system_channel is not(None):
                    if self.langs.find_one({"_id": before.id})["lang"] == "en":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Journal Audit | new rules channel")
                        embed.add_field(name="Old rules channel:", value=before.rules_channel)
                        embed.add_field(name="New rules channel:", value=after.rules_channel)
                        embed.set_footer(text=f"server id: {after.id}")
                        await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": before.id})["lang"] == "ru":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Журнал Аудита | Новый канал с правилами")
                        embed.add_field(name="Старый канал с правилами:", value=before.system_channel)
                        embed.add_field(name="Новый канал с правилами:", value=after.system_channel)
                        embed.set_footer(text=f"id сервера: {after.id}")
                        await channel_log.send(embed=embed)
                if before.verification_level != after.verification_level:
                    if self.langs.find_one({"_id": before.id})["lang"] == "en":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Journal Audit | new verification level")
                        embed.add_field(name="Old verification level:", value=before.verification_level)
                        embed.add_field(name="New verification level:", value=after.verification_level)
                        embed.set_footer(text=f"server id: {after.id}")
                        await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": before.id})["lang"] == "ru":
                        embed = discord.Embed(color=discord.Color.orange())
                        embed.set_author(name=f"Журнал Аудита | Новый уровень верификации")
                        embed.add_field(name="Старый уровень верификации:", value=before.verification_level)
                        embed.add_field(name="Новый уровень верификации:", value=after.verification_level)
                        embed.set_footer(text=f"id сервера: {after.id}")
                        await channel_log.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        idc = self.dateb.find_one({"_id": role.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": role.guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": role.guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": role.guild.id})["lang"] == "en":
                    description = f"Role permissions {role.mention}:\n**```diff\n"
                    for name, value in iter(role.permissions):
                        sym = "+" if value else "-"
                        description += f"{sym} {name}\n"

                    description += "```**"
                    embed = discord.Embed(description=f"Role name {role.name}\n{description}",color=discord.Color.random())
                    embed.set_author(name="Journal Audit | Create Role")
                    embed.set_footer(text=f"Role id: {role.id}")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": role.guild.id})["lang"] == "ru":
                    description = f"Права на роль {role.mention}:\n**```diff\n"
                    for name, value in iter(role.permissions):
                        sym = "+" if value else "-"
                        description += f"{sym} {name}\n"

                    description += "```**"
                    embed = discord.Embed(description=f"Название роли: {role.name}\n{description}",color=discord.Color.random())
                    embed.set_author(name="Журнал Аудита | Создание роли")
                    embed.set_footer(text=f"id роли: {role.id}")
                    await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        idc = self.dateb.find_one({"_id": role.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": role.guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": role.guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": role.guild.id})["lang"] == "en":
                    embed = discord.Embed(description=f"Removed Role: {role.name}",color=discord.Color.random())
                    embed.set_author(name="Journal Audit | Delete Role")
                    embed.set_footer(text=f"Role id: {role.id}")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": role.guild.id})["lang"] == "ru":
                    embed = discord.Embed(description=f"Удалённая роль: {role.name}",color=discord.Color.random())
                    embed.set_author(name="Журнал Аудита | Удаление роли")
                    embed.set_footer(text=f"id роли: {role.id}")
                    await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        idc = self.dateb.find_one({"_id": before.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": before.guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": before.guild.id})["lang"] == "en":
                    description = f"update role permissions {after.mention}:\n**```diff\n"
                    for name, value in iter(after.permissions):
                        sym = "+" if value else "-"
                        description += f"{sym} {name}\n"

                    description += "```**"
                    embed = discord.Embed(description=f"Old name {before.name}\nNew name {after.name}\n{description}",color=discord.Color.random())
                    embed.set_author(name="Journal Audit | Update Role")
                    embed.set_footer(text=f"Role id: {after.id}")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": before.guild.id})["lang"] == "ru":
                    description = f"Изменение права на роль {after.mention}:\n**```diff\n"
                    for name, value in iter(after.permissions):
                        sym = "+" if value else "-"
                        description += f"{sym} {name}\n"

                    description += "```**"
                    embed = discord.Embed(description=f"Старое Название роли: {before.name}\nНовое название роли: {after.name}\n{description}",color=discord.Color.random())
                    embed.set_author(name="Журнал Аудита | Обновление роли")
                    embed.set_footer(text=f"id роли: {after.id}")
                    await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        idc = self.dateb.find_one({"_id": guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": member.guild.id})["lang"] == "en":
                    embed = discord.Embed(description=f"User {member.name}({member.id}) has been banned.")
                    embed.set_author(name="Journal Audit | Ban Member")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": member.guild.id})["lang"] == "ru":
                    embed = discord.Embed(description=f"Пользователь {member.name}#{member.discriminator}({member.id}) был забанен")
                    embed.set_author(name="Журнал Аудита | Бан Участника")
                    await channel_log.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        idc = self.dateb.find_one({"_id": guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": guild.id})["lang"] == "en":
                    embed = discord.Embed(description=f"User {user.name}({user.id}) has been unbanned.")
                    embed.set_author(name="Journal Audit | Unban Member")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": guild.id})["lang"] == "ru":
                    embed = discord.Embed(description=f"Пользователь {user.name}#{user.discriminator}({user.id}) был разбанен")
                    embed.set_author(name="Журнал Аудита | Разбан Участника")
                    await channel_log.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        idc = self.dateb.find_one({"_id": invite.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": invite.guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": invite.guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": invite.guild.id})["lang"] == "en":
                    embed = discord.Embed(description=f"invite {invite.code} created. Invite url: {invite.url}")
                    embed.set_author(text="Journal Audit | Create invite")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": invite.guild.id})["lang"] == "ru":
                    embed = discord.Embed(description=f"Приглашение {invite.code} создано. Ссылка на инвайт: {invite.url}")
                    embed.set_author(text="Журнал Аудита | Создание приглашения")
                    await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        idc = self.dateb.find_one({"_id": invite.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": invite.guild.id})["setting"] == 2 or \
                self.dateb.find_one({"_id": invite.guild.id})["setting"] == 3:
                return False
            else:
                channel_log = self.bot.get_channel(idc)
                if self.langs.find_one({"_id": invite.guild.id})["lang"] == "en":
                    embed = discord.Embed(description=f"invite {invite.code} deleted. Invite url: {invite.url}")
                    embed.set_author(text="Journal Audit | Create invite")
                    await channel_log.send(embed=embed)
                elif self.langs.find_one({"_id": invite.guild.id})["lang"] == "ru":
                    embed = discord.Embed(description=f"Приглашение {invite.code} создано. Ссылка на инвайт: {invite.url}")
                    embed.set_author(text="Журнал Аудита | Создание приглашения")
                    await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild:
            idc = self.dateb.find_one({"_id": message.guild.id})["log"]
            if idc == 0:
                return False
            else:
                if self.dateb.find_one({"_id": message.guild.id})["setting"] == 3 or \
                    self.dateb.find_one({"_id": message.guild.id})["setting"] == 5:
                    return False
                else:
                    channel_log = self.bot.get_channel(idc)
                    if self.langs.find_one({"_id": message.guild.id})["lang"] == "en":
                        if len(str(message.content)) > 1900:
                            return await channel_log.send(file=discord.File(fp=io.StringIO(str(message.content)), filename="log.txt"))
                        embed = discord.Embed(description=f"{message.author.mention} Deleted message\nMessage:{message.content}\nChannel:{message.channel.mention}",color=discord.Color.random())
                        embed.set_author(name="Journal Audit | Removed message")
                        await channel_log.send(embed=embed)
                        for embed in message.embeds:
                            if len(str(embed.to_dict())) > 1900:
                                return await channel_log.send(file=discord.File(fp=io.StringIO(str(embed.to_dict())), filename="log.txt"))
                            descr = f"""
                            Message: {embed.to_dict()}
                            Author: {message.author.mention}
                            Channel: {message.channel}
                            """
                            embed = discord.Embed(description=descr, color=discord.Color.random())
                            embed.set_author(name="Journal Audit | Removed message")
                            embed.set_footer(text=f"Message ID: {message.id}")
                            await channel_log.send(embed=embed)
                        for sticker in message.stickers:
                            descr = f"""
                            Author: {message.author.mention}
                            Channel: {message.channel}
                            """
                            embed = discord.Embed(description=descr, color=discord.Color.random())
                            embed.set_thumbnail(url=sticker.image_url)
                            embed.set_author(name="Journal Audit | Removed message")
                            embed.set_footer(text=f"Message ID: {message.id}")
                    elif self.langs.find_one({"_id": message.guild.id})["lang"] == "ru":
                        embed = discord.Embed(description=f"{message.author.mention} Удалил сообщение\nСообщение:{message.content}\nКанал:{message.channel.mention}",color=discord.Color.random())
                        embed.set_author(name="Журнал Аудита | Удалённое сообщение")
                        await channel_log.send(embed=embed)
                        for embed in message.embeds:
                            if len(str(embed.to_dict())) > 1900:
                                return await channel_log.send(file=discord.File(fp=io.StringIO(str(embed.to_dict())), filename="log.txt"))
                            descr = f"""
                            Сообщение: {embed.to_dict()}
                            Автор: {message.author.mention}
                            Канал: {message.channel}
                            """
                            embed = discord.Embed(description=descr, color=discord.Color.random())
                            embed.set_author(name="Журнал Аудита | Удалённое сообщение")
                            embed.set_footer(text=f"ID сообщения: {message.id}")
                            await channel_log.send(embed=embed)
                        for sticker in message.stickers:
                            descr = f"""
                            Автор: {message.author.mention}
                            Канал: {message.channel}
                            """
                            embed = discord.Embed(description=descr, color=discord.Color.random())
                            embed.set_thumbnail(url=sticker.image_url)
                            embed.set_author(name="Журнал Аудита | Удалённое сообщение")
                            embed.set_footer(text=f"ID сообщения: {message.id}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        idc = self.dateb.find_one({"_id": before.guild.id}, {"log": before.channel.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.guild.id}, {"setting": 1 or 2})["setting"] == 1 or \
                    self.dateb.find_one({"_id": before.guild.id}, {"setting": 1 or 2})["setting"] == 2:
                if before.content != after.content:
                    channel_log = self.bot.get_channel(idc)
                    if self.langs.find_one({"_id": before.guild.id})["lang"] == "en":
                        if len(after.content) > 1950:
                            embed = discord.Embed(colour=discord.Colour.orange())
                            embed.set_author(name=f'Journal Audit | Message Edit')
                            embed.add_field(name="Author:", value=f"{before.author.name} ({before.author.id})")
                            embed.add_field(name="Channel:", value=f"<#{before.channel.id}>")
                            embed.add_field(name="Message", value="in File")
                            embed.set_footer(text=f"Message id: {before.id}")
                            return await channel_log.send(embed=embed, file=discord.File(fp=io.StringIO(str(embed.to_dict())), filename="log.txt"))
                        else:
                            embed = discord.Embed(colour=discord.Colour.orange())
                            embed.set_author(name=f'Journal Audit | Message Edit')
                            embed.add_field(name="Author:", value=f"{before.author.name} ({before.author.id})")
                            embed.add_field(name="Channel:", value=f"<#{before.channel.id}>")
                            embed.add_field(name="Old message:", value=f"{before.content}")
                            embed.add_field(name="New message:", value=f"{after.content}")
                            embed.set_footer(text=f"Message id: {before.id}")
                            await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": before.guild.id})["lang"] == "ru":
                        if len(after.content) > 1950:
                            embed = discord.Embed(colour=discord.Colour.orange())
                            embed.set_author(name=f'Журнал аудита | Изменённое сообщение')
                            embed.add_field(name="Автор:", value=f"{before.author.name} ({before.author.id})")
                            embed.add_field(name="Канал:", value=f"<#{before.channel.id}>")
                            embed.add_field(name="Сообщения", value="Файл с логом находится ниже")
                            embed.set_footer(text=f"id сообщения: {before.id}")
                            return await channel_log.send(embed=embed, file=discord.File(fp=io.StringIO(str(embed.to_dict())), filename="log.txt"))
                        else:
                            embed = discord.Embed(colour=discord.Colour.orange())
                            embed.set_author(name=f'Журнал аудита | Изменённое сообщение')
                            embed.add_field(name="Автор:", value=f"{before.author.name} ({before.author.id})")
                            embed.add_field(name="Канал:", value=f"<#{before.channel.id}>")
                            embed.add_field(name="Старое сообщение:", value=f"{before.content}")
                            embed.add_field(name="Изменёное сообщение:", value=f"{after.content}")
                            embed.set_footer(text=f"id сообщения: {before.id}")
                            await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        idc = self.dateb.find_one({"_id": channel.guild.id}, {"log": channel.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": channel.guild.id}, {"setting": 1 or 2})["setting"] == 1 or \
                    self.dateb.find_one({"_id": channel.guild.id}, {"setting": 1 or 2})["setting"] == 2:
                    channel_log = self.bot.get_channel(idc)
                    if self.langs.find_one({"_id": channel.guild.id})["lang"] == "en":
                        embed=discord.Embed(description=f"Channel name: {channel.name}\nChannel: {channel.mention}\nCreated: {channel.created_at.strftime('%d.%m.%y %H:%M:%S')}")
                        embed.set_author(name=f"Journal Audit | Create channel")
                        embed.set_footer(text=f"Channel id {channel.id}")
                        await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": channel.guild.id})["lang"] == "ru":
                        embed=discord.Embed(description=f"Название канала: {channel.name}\nКанал: {channel.mention}\nСоздан: {channel.created_at.strftime('%d.%m.%y %H:%M:%S')}")
                        embed.set_author(name=f"Журнал Аудита | Создание канала")
                        embed.set_footer(text=f"id канала {channel.id}")
                        await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        idc = self.dateb.find_one({"_id": channel.guild.id}, {"log": channel.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": channel.guild.id}, {"setting": 1 or 2})["setting"] == 1 or \
                    self.dateb.find_one({"_id": channel.guild.id}, {"setting": 1 or 2})["setting"] == 2:
                    channel_log = self.bot.get_channel(idc)
                    if self.langs.find_one({"_id": channel.guild.id})["lang"] == "en":
                        embed=discord.Embed(description=f"Channel name: {channel.name}\nHas been Created: {channel.created_at.strftime('%d.%m.%y %H:%M:%S')}")
                        embed.set_author(name=f"Journal Audit | Delete channel")
                        await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": channel.guild.id})["lang"] == "ru":
                        embed=discord.Embed(description=f"Название канала: {channel.name}\nБыл Создан: {channel.created_at.strftime('%d.%m.%y %H:%M:%S')}")
                        embed.set_author(name=f"Журнал Аудита | Удаление канала")
                        embed.set_footer(text=f"id канала {channel.id}")
                        await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        idc = self.dateb.find_one({"_id": after.guild.id}, {"log": before.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": before.guild.id}, {"setting": 1 or 2})["setting"] == 1 or \
                    self.dateb.find_one({"_id": before.guild.id}, {"setting": 1 or 2})["setting"] == 2:
                    channel_log = self.bot.get_channel(idc)
                    if self.langs.find_one({"_id": before.guild.id})["lang"] == "en":
                        if before.name != after.name:
                            embed=discord.Embed(description=f"Old channel name: {before.name}\nNew channel name: {after.name}")
                            embed.set_footer(text=f"Channel id {after.id}")
                            embed.set_author(name=f"Journal Audit | Update channel")
                            await channel_log.send(embed=embed)
                    elif self.langs.find_one({"_id": before.guild.id})["lang"] == "ru":
                        if before.name != after.name:
                            embed=discord.Embed(description=f"Старое название канала: {before.name}\nНовое название канала: {after.name}")
                            embed.set_author(name=f"Журнал Аудита | Обновление канала")
                            embed.set_footer(text=f"id канала {after.id}")
                            await channel_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before=None, after=None):
        idc = self.dateb.find_one({"_id": member.guild.id})["log"]
        if idc == 0:
            return False
        else:
            if self.dateb.find_one({"_id": member.guild.id})["setting"] == 2 or \
                    self.dateb.find_one({"_id": member.guild.id})["setting"] == 5:
                return False
            else:
                if after.channel is None:
                    if not before.channel is None:
                        if member.bot:
                            return
                        channel = self.bot.get_channel(idc)  # Сюда свой канал логов
                        e = discord.Embed(
                            description=f'**Пользователь {member.display_name}({member.mention}) вышел из голосового '
                                        f'канала 🔊**',
                            colour=discord.Colour.orange())
                        e.set_author(name=f'Журнал аудита | Выход из канала')
                        e.add_field(name="Предыдущий канал",
                                    value=f"**{before.channel.name}({before.channel.mention})**")
                        e.add_field(name="ID Участника", value=f"**{member.id}**")
                        return await channel.send(embed=e)

                if (not before.channel is None) and (not after.channel is None):
                    if before.channel.id is after.channel.id:
                        return

                    if member.bot:
                        return
                    channel = self.bot.get_channel(idc)  # Сюда свой канал логов
                    e = discord.Embed(
                        description=f'**Пользователь {member.display_name}({member.mention}) перешёл в другой '
                                    f'голосовой канал 🔊**',
                        colour=discord.Colour.orange())
                    e.set_author(name=f'Журнал аудита | Переход в канал')
                    e.add_field(name="Действующий канал", value=f"**{after.channel.name}({after.channel.mention})**")
                    e.add_field(name="Предыдущий канал", value=f"**{before.channel.name}({before.channel.mention})**")
                    e.add_field(name="ID Участника", value=f"**{member.id}**")
                    return await channel.send(embed=e)

                if not after.channel is None:
                    if before.channel is None:
                        if member.bot:
                            return
                        channel = self.bot.get_channel(idc)  # Сюда ид канала логов
                        e = discord.Embed(
                            description=f'**Пользователь {member.display_name}({member.mention}) зашёл в голосовой '
                                        f'канал 🔊**',
                            colour=discord.Colour.orange())
                        e.set_author(name=f'Журнал аудита | Вход в канал')
                        e.add_field(name="Действующий канал",
                                    value=f"**{after.channel.name}({after.channel.mention})**")
                        e.add_field(name="ID Участника", value=f"**{member.id}**")
                        return await channel.send(embed=e)


    # @commands.Cog.listener()
    # async def on_guild_channel_create(self, channel):
    #     idc = self.dateb.find_one()["log"]
    #     if idc == 0:
    #         return False
    #     else:
    #         if self.dateb.find_one()["setting"] == 2 or \
    #                 self.dateb.find_one()["setting"] == 3 or \
    #                 self.dateb.find_one()["setting"] == 4:
    #             return False
    #         else:
    #             chanel = self.bot.get_channel(idc)  # Сюда ид канала логов
    #             async for entry in chanel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
    #                 if entry.user.bot:
    #                     return
    #                 else:
    #                     e = discord.Embed(colour=discord.Colour.orange())
    #                     e.set_author(name='Журнал аудита | Создание канала')
    #                     e.add_field(name="Канал:", value=f"<#{entry.target.id}>")
    #                     e.add_field(name="ID Канала:", value=f"{entry.target.id}")
    #                     e.add_field(name="Создал:", value=f"{entry.user.mention} ({entry.user.id})")
    #                     await chanel.send(embed=e)
    #                     return

    # @commands.Cog.listener()
    # async def on_guild_channel_delete(self, channel):
    #     idc = self.dateb.find_one()["log"]
    #     if idc == 0:
    #         return False
    #     else:
    #         if self.dateb.find_one()["setting"] == 2 or \
    #                 self.dateb.find_one()["setting"] == 3 or \
    #                 self.dateb.find_one()["setting"] == 4:
    #             return False
    #         else:
    #             chanel = self.bot.get_channel(idc)  # Сюда ид канала логов
    #             async for entry in chanel.guild.audit_logs(action=discord.AuditLogAction.channel_delete):
    #                 if entry.user.bot:
    #                     return
    #                 else:
    #                     e = discord.Embed(colour=discord.Colour.orange())
    #                     e.set_author(name='Журнал аудита | Удаление канала')
    #                     e.add_field(name="Канал:", value=f"{channel.name}")
    #                     e.add_field(name="ID Канала:", value=f"{entry.target.id}")
    #                     e.add_field(name="Удалил:", value=f"{entry.user.mention} ({entry.user.id})")
    #                     return await chanel.send(embed=e)

    # @commands.Cog.listener()
    # async def on_guild_role_create(self, role):
    #     idc = self.dateb.find_one()["log"]
    #     if idc == 0:
    #         return False
    #     else:
    #         if self.dateb.find_one()["setting"] == 2 or \
    #                 self.dateb.find_one()["setting"] == 3 or \
    #                 self.dateb.find_one()["setting"] == 4:
    #             return False
    #         else:
    #             chanel = self.bot.get_channel(idc)  # Сюда ид канала логов
    #             async for entry in chanel.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
    #                 e = discord.Embed(colour=discord.Colour.orange())
    #                 e.set_author(name='Журнал аудита | Создание роли')
    #                 e.add_field(name="Роль:", value=f"<@&{entry.target.id}>")
    #                 e.add_field(name="ID роли:", value=f"{entry.target.id}")
    #                 e.add_field(name="Создал:", value=f"{entry.user.mention} ({entry.user.id})")
    #                 await chanel.send(embed=e)
    #                 return

    # @commands.Cog.listener()
    # async def on_guild_role_delete(self, role):
    #     idc = self.dateb.find_one()["log"]
    #     if idc == 0:
    #         return False
    #     else:
    #         if self.dateb.find_one()["setting"] == 2 or \
    #                 self.dateb.find_one()["setting"] == 3 or \
    #                 self.dateb.find_one()["setting"] == 4:
    #             return False
    #         else:
    #             chanel = self.bot.get_channel(idc)  # Сюда ид канала логов
    #             async for entry in chanel.guild.audit_logs(action=discord.AuditLogAction.role_delete):
    #                 e = discord.Embed(colour=discord.Colour.orange())
    #                 e.set_author(name='Журнал аудита | Удаление роли')
    #                 e.add_field(name="Роль:", value=f"{role.name}")
    #                 e.add_field(name="ID роли:", value=f"{entry.target.id}")
    #                 e.add_field(name="Удалил:", value=f"{entry.user.mention} ({entry.user.id})")
    #                 return await chanel.send(embed=e)


def setup(bot):
    bot.add_cog(Logs(bot))
