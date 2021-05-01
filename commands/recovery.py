import discord
import sys
from discord.ext import commands
import os


class RecoveryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('🐺Админ', '🦊 Moder')
    async def panel(self, ctx):
        await ctx.message.delete()

        member = discord.Member = "694598900094599198"
        member = discord.Member = "443484756613660674"
        embed_recovery = discord.Embed(title=f"{self.bot.user.name} | Панель управления")
        embed_recovery.set_thumbnail(url=ctx.author.avatar_url)

        embed_recovery.add_field(name=':',
                                 value="\n"
                                       "**Острожно!**\n"
                                       "*Если вы нажмёте на 💥 то файлы бота удалятся!* \n"
                                       "*Спасибо за внимание...*",
                                 inline=False)
        embed_recovery.add_field(name='Выберите реакцию:',
                                 value=f'⭕ __**Перезапуск**__\n'
                                       f'❌ __**Выключение**__\n'
                                       f'========================\n'
                                       f'♦ __**Backup**__\n'
                                       f'========================\n'
                                       f'💥 __**Полное удаление бота**__', inline=False)
        msg = await ctx.send(embed=embed_recovery)
        await msg.add_reaction("⭕")
        await msg.add_reaction("❌")
        await msg.add_reaction("♦")
        await msg.add_reaction("💥")
        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0,
                                                 check=lambda reaction, user: user.id == ctx.author.id and str(
                                                     reaction.emoji) in ["⭕", "❌", "♦", "💥",
                                                                         ""] and reaction.message.id == msg.id)

        if str(reaction.emoji) == "⭕":
            embed_reload = discord.Embed(title=f"{self.bot.user.name} | Control Panel")
            embed_reload.set_thumbnail(url=ctx.author.avatar_url)
            embed_reload.add_field(name="⭕ __**Перезагрузка**__",
                                   value=f"{ctx.author.mention}, начинаю перезапуск. . .")
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    if filename == 'recovery.py':
                        pass
                    else:
                        self.bot.unload_extension(f'commands.{filename[0:-3]}')
                        self.bot.load_extension(f'commands.{filename[0:-3]}')
            for filename2 in os.listdir('./events'):
                if filename2.endswith('.py'):
                    self.bot.unload_extension(f'events.{filename2[0:-3]}')
                    self.bot.load_extension(f'events.{filename2[0:-3]}')
            embed_reload_complete = discord.Embed(title=f"{self.bot.user.name} | Control Panel")
            embed_reload_complete.set_thumbnail(url=ctx.author.avatar_url)
            embed_reload_complete.add_field(name="⭕ __**Перезагрузка**__",
                                            value=f"{ctx.author.mention}, перезапуск завершен!", inline=False)
            embed_reload_complete.add_field(name="__**Совет**__:", value="для подробностей проверьте «Журнал Системы».",
                                            inline=False)

            await msg.edit(embed=embed_reload)
            embed = discord.Embed(
                title="Перезапуск. . .",
                color=0x808080,
                timestamp=ctx.message.created_at
            )
            await msg.edit(embed=embed_reload_complete, delete_after=15)
            print("\nПерезапущено!\n")
        elif str(reaction.emoji) == "❌":
            embed_shutdown = discord.Embed(title='Выход...6  ', color=000000)
            await msg.edit(embed=embed_shutdown)
            sys.exit(0)
        elif str(reaction.emoji) == "♦":
            embed_recovery_cmd = discord.Embed(title='rc', color=000000)
            await msg.edit(embed=embed_recovery_cmd)
        elif str(reaction.emoji) == "💥":
            embed_boom = discord.Embed(title='boom', color=000000)
            await msg.edit(embed=embed_boom)
        else:
            await ctx.send('Error: none emoji')


def setup(bot):
    bot.add_cog(RecoveryCog(bot))
