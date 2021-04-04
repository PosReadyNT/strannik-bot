import os
import discord
import asyncio
from discord import Template
import youtube_dl
from discord.voice_client import VoiceClient
from config import config
from utils.mongo import Document
import motor.motor_asyncio
from discord.ext import commands
import googletrans
from googletrans import Translator
from discord.ext.commands import when_mentioned_or
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions, errors

bot = commands.Bot(command_prefix = commands.when_mentioned_or("s.", "strannik.", "/"), intents = discord.Intents.all())
bot.remove_command('help')

@bot.command()
async def translate(ctx, lang_to, *args):
    import googletrans
    from google_trans_new import google_translator  

    if lang_to not in googletrans.LANGCODES:
        embed = discord.Embed(
            description = f':x: {ctx.author.mention}, данного **языка** не существует, я отправлю список **языков** тебе в **лс** :x:',
            color = 0xff0000)

        embed.set_author(icon_url='https://www.flaticon.com/premium-icon/icons/svg/1828/1828665.svg',
                        name = 'Перевод | Ошибка')
        embed.set_footer(text = f'{bot.user.name} © 2021 | Все права защищены', icon_url = bot.user.avatar_url)

        await ctx.send(embed = embed)

        languages = ", ".join(googletrans.LANGUAGES)

        embed = discord.Embed(description = f'**Список всех языков:** {languages}',
                                color = 0x00FF00)

        embed.set_footer(text = f'{bot.user.name} © 2021 | Все права защищены', icon_url = bot.user.avatar_url)

        await ctx.author.send(embed = embed)
    else:
        translator = google_translator()  
        result = translator.translate(" ".join(args),lang_tgt=lang_to)  

        embed = discord.Embed(title = '**Перевод твоего сообщения**',
                        description = f"**Твое сообщение:** - {' '.join(args)}\n\n**Перевод:** - {result}\n\n",
                        color = 0x00FF00)
        embed.set_footer(text = f'{bot.user.name} © 2021 | Все права защищены', icon_url = bot.user.avatar_url)
        embed.set_thumbnail(
            url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Google_Translate_logo_%28old%29.png')

        msg = await ctx.send(embed = embed)
        await msg.add_reaction("🗑️")
        reaction, user = await bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
        if str(reaction.emoji) == "🗑️":
            await msg.clear_reactions()
            await ctx.message.delete()
        else:
            return False

@bot.command()
async def unload(ctx, extins):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        bot.unload_extension(f'commands.{extins}')
        await ctx.send("OK!")
    else:
        return False

@bot.command()
async def load(ctx, extins):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        bot.load_extension(f'commands.{extins}')
        await ctx.send("OK!")
    else:
        return False

@bot.command()
async def logout(ctx):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        await ctx.send("OK!")
        await bot.logout()
    else:
        return False

@bot.command()
async def reload_bot(ctx):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        await ctx.send("OK!")
        await bot.logout()
        #os.system("D:")
        #os.system("D:/BACKUP/vashnoe/Projects Python/strannikbot")
        os.system("python bot.py")
    else:
        return False

@bot.command()
async def reload(ctx, extins):
    if ctx.author.id == 694598900094599198 or ctx.author.id == 443484756613660674:
        bot.unload_extension(f'commands.{extins}')
        bot.load_extension(f'commands.{extins}')
        await ctx.send("OK!")
    else:
        return False

if __name__ == "__main__":
    for filename in os.listdir('./events'):
        if filename.endswith('.py'):
            bot.load_extension(f'events.{filename[:-3]}')
        if filename.endswith('.pyw'):
            os.system(f"rename {filename} {filename[:-1]}")
            bot.load_extension(f'events.{filename[:-3]}')

    for filename2 in os.listdir('./commands'):
        if filename2.endswith('.py'):
            bot.load_extension(f'commands.{filename2[:-3]}')
        if filename2.endswith('.pyw'):
            os.system(f"rename {filename2} {filename2[:-1]}")
            bot.load_extension(f'commands.{filename2[:-3]}')

    bot.run(config["token"])