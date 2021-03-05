import os
import discord
from config import config
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions, errors

bot = commands.Bot(command_prefix = commands.when_mentioned_or("s."), intents = discord.Intents.all())
bot.remove_command('help')

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