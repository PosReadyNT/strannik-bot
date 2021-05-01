import discord
from discord.ext import commands
from pymongo import MongoClient
import io
import os
from config import config as conf


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clust = MongoClient(conf["mongo_db"])
        self.reports = self.clust["posready"]["reports"]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def report_channel(self, ctx, on=None, channel: discord.TextChannel = None):
        def colladd():
            post = {
                "_id": ctx.guild.id,
                "report": 0
            }
            self.reports.insert_one(post)
        if on is "off":
            self.reports.delete_one({"_id": ctx.guild.id})
            embed = discord.Embed(
                title="Репорт канал",
                description=f"Канал для жалоб был отключен",
                color=discord.Color.from_rgb(110, 196, 86)
            )
            msg = await ctx.reply(embed=embed)
            await msg.add_reaction('❌')
        else:
            self.reports.insert_one({"_id": ctx.guild.id, "report": 0})
            self.reports.update_one({"_id": ctx.guild.id}, {"$set": {"report": channel.id}})

            embed = discord.Embed(
                title="Репорт канал",
                description=f"Канал для жалоб был обновлён на: {channel.mention}. Для использования команды для жалоб пишите: `s.report @user#1234 причина <необязательно: скриншот>`",
                color=discord.Color.from_rgb(110, 196, 86))

            msg = await ctx.reply(embed=embed)
            await msg.add_reaction('✅')

    @commands.command()
    async def report(self, ctx, member: discord.Member = None, *, reportarg: str = None):
        if member is None:
            await ctx.send("Введите участника, который нарушил!")
        elif reportarg is None or reportarg is '':
            await ctx.send("Введите аргумент для жалобы!")
        else:
            if self.reports.find_one({"_id": ctx.guild.id})["report"] != 0:
                await ctx.send("Жалоба отправлена!")
                a = self.reports.find_one({"_id": ctx.guild.id})["report"]
                ab = self.bot.get_channel(a)
                embed = discord.Embed(title="Жалоба",description=f"Поступила жалоба от {ctx.author.mention}\nна {member.mention}\n\n"f"Причина жалобы: {reportarg}",color=discord.Color.red())
                if ctx.message.attachments:
                    for files in ctx.message.attachments:
                        embed.set_image(url=f"{files.url}")
                await ab.send(embed=embed)

def setup(bot):
    bot.add_cog(Report(bot))
