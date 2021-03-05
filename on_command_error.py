import os
import discord
from config import config
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions, errors

class Command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.event
    async def on_command_error(ctx, error):

        emb = discord.Embed(title = "Error",
            description = f"```css\n{error}\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.",
            colour = discord.Colour.red(),
            timestamp = ctx.message.created_at)
        emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.BadArgument):
    
            if "Member" in str(error):
    
                embed = discord.Embed(title = "Error",
                    description = f'```ini\n[ данного участника не существует ]\n``\nJoin the [support server](https://discord.gg/cCr49tm) for help.',
                    color = discord.Colour.red(),
                    timestamp = ctx.message.created_at)
                embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

                return await ctx.send(embed = embed)
    
            if "Guild" in str(error):
    
                embed = discord.Embed(title = "Error",
                    description = f'```ini\n[ данного сервера, не существует ]\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.',
                    color = discord.Colour.red(),
                    timestamp = ctx.message.created_at)
                embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
    
                return await ctx.send(embed = embed)
    
            else:
                embed = discord.Embed(title = "Error",
                    description = f'```ini\n[ не верный агрумент ]\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.',
                    color = discord.Colour.red(),
                    timestamp = ctx.message.created_at)
                embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

                return await ctx.send(embed = embed)
    
        if isinstance(error, commands.MissingRequiredArgument):
    
            embed = discord.Embed(title = "Error",
                description = f'```ini\n[ пропущен аргумент с названием {error.param.name} ]\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.',
                color = discord.Colour.red(),
                timestamp = ctx.message.created_at)
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
    
            return await ctx.send(embed = embed)

        if isinstance(error, errors.BotMissingPermissions):
            
            embed = discord.Embed(title = "Error",
                description=f"```ini\n[ У бота отсутствуют права: {' '.join([str(i) for i in error.missing_perms])} ]\n```\nВыдайте их ему для полного функционирования бота\nJoin the [support server](https://discord.gg/cCr49tm) for help.",
                color = discord.Colour.red(),
                timestamp = ctx.message.created_at)
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
    
            return await ctx.send(embed = embed)

        if isinstance(error, errors.MissingPermissions):

            embed = discord.Embed(title = "Error",
                description=f"```ini\n[ У вас недостаточно прав для запуска этой команды! ]\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.",
                color = discord.Colour.red(),
                timestamp = ctx.message.created_at)
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

            return await ctx.send(embed = embed)

        if isinstance(error, commands.CommandOnCooldown):
            
            embed = discord.Embed(title = "Error",
                description=f"```ini\n[ У вас еще не прошел кулдаун на команду {ctx.command}!\nПодождите еще {error.retry_after:.2f} ]\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.",
                color = discord.Colour.red(),
                timestamp = ctx.message.created_at)
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

            return await ctx.send(embed = embed)

        if isinstance(error, dpy_errors.Forbidden):
            
            embed = discord.Embed(title = "Error",
                description=f"```ini\n[ У бота нет прав на запуск этой команды! ]\n```\nJoin the [support server](https://discord.gg/cCr49tm) for help.",
                color = discord.Colour.red(),
                timestamp = ctx.message.created_at)
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

            return await ctx.send(embed = embed)

        if isinstance(error, commands.MaxConcurrencyReached):
            return

        else:
            await ctx.send(embed = emb)


def setup(bot):
    bot.add_cog(Command_error(bot))