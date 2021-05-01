import discord
from discord_slash import SlashCommand, cog_ext
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="все команды (чтобы увидеть всю справку, вводите без аргумента)")
    async def help(self, ctx, arg = None):
        prefix = "s."
        if arg is None:
            embed = discord.Embed(title = "Справка по командам", description="```css\n[] - агрумент (Иногда важно)\n<> - опция (on/off) (обязательно, но появляется редко)```", colour = discord.Colour.green())
            embed.add_field(name="Настройки", value=f"{prefix}help settings", inline=False)
            embed.add_field(name="Музыка", value=f"{prefix}help music", inline=False)
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.send(embed=embed)
        elif arg == "settings":
            embed = discord.Embed(title = "Справка по командам", description="```css\n[] - агрумент (Иногда важно)\n<> - опция (on/off) (обязательно, но появляется редко)\n<#> - ввод канала (Обязателен)```", colour = discord.Colour.green())
            embed.add_field(name="Лог канал", value=f"{prefix}logchannel <on/off> <#>", inline=False)
            embed.add_field(name="Репорты", value=f"{prefix}report_channel <on/off> <#>", inline=False)
            embed.add_field(name="Приветствие участника", value=f"{prefix}member_join <on/off> <#>", inline=False)
            embed.add_field(name="Уход участника", value=f"{prefix}member_leave <on/off> <#>", inline=False)
            embed.add_field(name="Дурка роль", value=f"{prefix}durka_role @role", inline=False)
            embed.add_field(name="Включить автороль", value=f"{prefix}autorole @role", inline=False)
            embed.add_field(name="Отключить автороль", value=f"{prefix}autorole_delete", inline=False)
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.send(embed=embed)
        elif arg == "music":
            embed = discord.Embed(title = "Справка по командам", description="```css\n<url/name> - ссылка или название видео\n<#> - ввод канала (Обязателен)```", colour = discord.Colour.green())
            embed.add_field(name="Вход в голосовой канал", value=f"{prefix}join <#>", inline=False)
            embed.add_field(name="Выход из голосового канала", value=f"{prefix}leave", inline=False)
            embed.add_field(name="Играть музыку", value=f"{prefix}play <url/name>", inline=False)
            embed.add_field(name="Пауза", value=f"{prefix}pause", inline=False)
            embed.add_field(name="Убрать паузу", value=f"{prefix}resume", inline=False)
            embed.add_field(name="Пропустить", value=f"{prefix}skip", inline=False)
            embed.add_field(name="Изменение звука", value=f"{prefix}volume <от 0 до 100>", inline=False)
            embed.add_field(name="Посмотреть, что сейчас играет", value=f"{prefix}current", inline=False)
            embed.add_field(name="Посмотреть список песен", value=f"{prefix}queue", inline=False)
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Help(bot))