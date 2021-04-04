import discord
from discord.ext import commands
from pymongo import MongoClient
from config import config as conf

class Report(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.clust = MongoClient(conf["mongo_db"])
        self.reports = self.clust["posready"]["reports"]
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def report_channel(self, ctx, on=None, channel: discord.TextChannel=None):
        def colladd():
            post = {
                "_id": ctx.guild.id,
                "report": 0
            }
            self.reports.insert_one(post)
        if on == None:
            await ctx.send("Введите слово (on - включить/off - выключить)")
        if on == "off":
            if ctx.guild.id == 767096403549487124:
                self.reports.update_one({"_id": ctx.guild.id}, {"$set": {"report": 0}})
                embed = discord.Embed(
                    title = "Репорт канал", 
                    description = f"Канал для жалоб был отключен", 
                    color = discord.Color.from_rgb(110, 196, 86)
                )
                msg = await ctx.reply(embed=embed)
                await msg.add_reaction('❌')
            else:
                self.reports.delete_one({"_id": ctx.guild.id})
                embed = discord.Embed(
                    title = "Репорт канал", 
                    description = f"Канал для жалоб был отключен",
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
                    self.reports.update_one({"_id": ctx.guild.id}, {"$set": {"report": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Репорт канал", 
                        description = f"Канал для жалоб был обновлён на: {channel.mention}",
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
                else:
                    colladd()
                    self.reports.update_one({"_id": ctx.guild.id}, {"$set": {"report": channel.id}})
                        
                    embed = discord.Embed(
                        title = "Репорт канал", 
                        description = f"Канал для жалоб был обновлён на: {channel.mention}",
                        color = discord.Color.from_rgb(110, 196, 86))
                    
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction('✅')
    
    @commands.command()
    async def report(self, ctx, member: discord.Member = None, *, reportarg: str = None):
        if member == None:
            await ctx.send("Введите участника, который нарушил!")
        elif reportarg == None or reportarg == '':
            await ctx.send("Введите аргумент для жалобы!")
        else:
            if self.reports.find_one({"_id": ctx.guild.id})["report"] != 0:
                await ctx.send("Жалоба отправлена!")
                a = self.reports.find_one({"_id": ctx.guild.id})["report"]
                ab = self.bot.get_channel(a)
                embed = discord.Embed(title="Жалоба", description=f"Поступила жалоба от {ctx.author.mention}\nна {member.mention}\n\nПричина жалобы: {reportarg}", color=discord.Color.red())
                await ab.send(embed=embed)

def setup(bot):
    bot.add_cog(Report(bot))