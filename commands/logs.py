import discord
from pymongo import MongoClient
from config import config as conf
from discord.ext import commands

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
                        description = f"Канал для логирования сервера был обновлён на: {channel.mention}", 
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
                else:
                    colladd()
                    self.dateb.update_one({"_id": ctx.guild.id}, {"$set": {"log": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Лог канал", 
                        description = f"Канал для логирования сервера был обновлён на: {channel.mention}", 
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        idc = self.dateb.find_one({"_id": before.guild.id}, {"log": before.channel.id})["log"]
        if idc == 0:
            return False
        else:
            channel_log = self.bot.get_channel(idc)
            embed = discord.Embed(title="Логи", description=f"{before.author.name} Изменил сообщение")
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
            channel_log = self.bot.get_channel(idc)
            embed = discord.Embed(title="Логи", description=f"{message.author.name} Удалил сообщение")
            embed.add_field(name="Удалённое сообщение:", value=f"{message.content}")
            embed.set_footer(text=f"id сообщения: {message.id}")
            await channel_log.send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))