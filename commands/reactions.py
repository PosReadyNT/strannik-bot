import discord
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.reaction_roles = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for role_id, msg_id, emoji in self.bot.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(role_id))
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        for role_id, msg_id, emoji in self.bot.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                guild = self.bot.get_guild(payload.guild_id)
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
                return

    @commands.command(description="Добавить эмодзи в сообщение и сделать его как роль", usage="<Имя роли> <id сообщения> <реакция>")
    async def set_reaction(self, ctx, role: discord.Role = None, msg: discord.Message = None, emoji=None):
        if role != None and msg != None and emoji != None:
            await msg.add_reaction(emoji)
            self.bot.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))
    
            await ctx.channel.send("Успешно поставлено!")
        else:
            await ctx.send("Ошибка!")
                

def setup(bot):
    bot.add_cog(Reactions(bot))