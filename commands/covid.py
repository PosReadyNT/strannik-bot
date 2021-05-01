import json
import requests
import discord
from discord_slash import SlashCommand, cog_ext
from discord.ext import commands

class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="covid", description="Просмотр заболевших ковидом (Страны на русском работают)")
    async def covid(self, ctx, country):
        def cov_country(country):
            country = country.lower()
            if country == "россия":
                return "Russia"
            elif country == "украина":
                return "Ukraine"
            elif country == "аргентина":
                return "Argentina"
            elif country == "австралия":
                return "Australia"
            elif country == "бразилия":
                return "Brazil"
            elif country == "китай":
                return "China"
            elif country == "египет":
                return "Egypt"
            elif country == "англия":
                return "England"
            elif country == "эстония":
                return "Estonia"
            elif country == "франция":
                return "France"
            elif country == "германия":
                return "Germany"
            elif country == "ирландия":
                return "Ireland"
            elif country == "израиль":
                return "Israel"
            elif country == "италия":
                return "Italy"
            elif country == "япония":
                return "Japan"
            elif country == "латвия":
                return "Latvia"
            elif country == "литва":
                return "Lithuania"
            elif country == "мексика":
                return "Mexico"
            elif country == "новая зеландия":
                return "New Zealand"
            elif country == "польша":
                return "Poland"
            elif country == "португалия":
                return "Portugal"
            elif country == "румыния":
                return "Romania"
            elif country == "шотландия":
                return "Scotland"
            elif country == "испания":
                return "Spain"
            elif country == "швейцария":
                return "Switzerland"
            elif country == "таиланд":
                return "Thailand"
            elif country == "чешская республика" or country == "чехия":
                return "CZ"
            elif country == "соединенное королевство великобритании и северной ирландии" or country == "великобритания":
                return "UK"
            elif country == "соединенные штаты америки" or country == "сша":
                return "USA"
            elif country == "турция":
                return "Turkey"

        for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
            if item['country'] == cov_country(country):
                embed = discord.Embed(title=f'Статистика Коронавируса | {country}')
                embed.add_field(name='Выздоровело:',          value=f'{item["recovered"]} человек')
                embed.add_field(name='Заболеваний:',          value=f'{item["cases"]} человек')
                embed.add_field(name='Погибло:',              value=f'{item["deaths"]} человек')
                embed.add_field(name='Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
                embed.add_field(name='Погибло за сутки:',     value=f'+{item["todayDeaths"]} человек')
                embed.add_field(name='Проведено тестов:',     value=f'{item["tests"]} человек')
                embed.add_field(name='Активные зараженные:',  value=f'{item["active"]} человек')
                embed.add_field(name='В тяжелом состоянии:',  value=f'{item["critical"]} человек')
                embed.set_thumbnail(url=item["countryInfo"]['flag'])
                embed.set_footer(text=f"© Copyright {self.bot.user.name} 2021 | Все права у меня")

                return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Covid(bot))