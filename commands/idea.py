import discord
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext
class Idea(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="idea",description='Отправить идею для бота')
    async def idea(self, ctx, name:str, idea: str):
        if name == '' or name == ' ':
            await ctx.send("Введите название идеи!")
        elif idea == '' or idea == ' ':
            await ctx.send("Введите описание идеи!")
        elif idea == '' or idea == ' ' and name == '' or name == ' ':
            await ctx.send("Введите название и описание идеи!")
        else:
            msg = await ctx.send(f"Вы уверены отправить идею?\nНазвание Идеи: {name}\nИдея: {idea}")
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction, user = await self.bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["✅","❌"] and reaction.message.id == msg.id)
            if str(reaction.emoji) == "✅":
                await msg.clear_reactions()
                developer1 = self.bot.get_user(835943271746371595)
                developer2 = self.bot.get_user(443484756613660674)
                global member
                member = ctx.author.id
                embed = discord.Embed(title="Новая идея!", description=f"Пришла новая идея!\nНазвание: {name}\nОписание: {idea}")
                embed.set_footer(text=f"id отправителя: {ctx.author.id}")
                await developer1.send(embed=embed)
                msg = await developer1.send("Вы согласны принять его? (Напишите: Да или Нет)")
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
                reaction, user = await self.bot.wait_for("reaction_add",check=lambda reaction,user: user.id == developer1.id and str(reaction.emoji) in ["✅","❌"] and reaction.message.id == msg.id)
                if str(reaction.emoji) == "✅":
                    #idea_channel = self.bot.get_channel()
                    member = self.bot.get_user(member)
                    member_mess = await member.send("Вашу идею приняли. Поздравляем 🥳")
                    await member_mess.add_reaction("✅")
                elif str(reaction.emoji) == "❌":
                    member2 = self.bot.get_user(member)
                    member_mess = await member2.send("Вашу идею отклонили. 😢")
                    await member_mess.add_reaction("❌")
                else:
                    return False
                await developer2.send(embed=embed)
                msg3 = await developer1.send("Вы согласны принять его? (Напишите: Да или Нет)")
                await msg3.add_reaction("✅")
                await msg3.add_reaction("❌")
                reaction, user = await self.bot.wait_for("reaction_add",check=lambda reaction,user: user.id == developer2.id and str(reaction.emoji) in ["✅","❌"] and reaction.message.id == msg.id)
                if str(reaction.emoji) == "✅":
                    #idea_channel = self.bot.get_channel()
                    member = self.bot.get_user(member)
                    member_mess = await member.send("Вашу идею приняли. Поздравляем 🥳")
                    await member_mess.add_reaction("✅")
                elif str(reaction.emoji) == "❌":
                    member2 = self.bot.get_user(member)
                    member_mess = await member2.send("Вашу идею отклонили. 😢")
                    await member_mess.add_reaction("❌")
                else:
                    return False
            elif str(reaction.emoji) == "❌":
                await msg.clear_reactions()
                await ctx.send("Ок, я не отправил разработчикам идею.")

def setup(bot):
    bot.add_cog(Idea(bot))