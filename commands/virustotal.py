import requests
import json
from discord.ext import commands


class Virustotal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="virus-scan")
    async def virustotal(self, ctx, *, url):
        api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
        params = dict(apikey='a0fe4114e9b365b373cb6d5fa41d1cb63c06f4f00de655f38cd73db4bde3bbcf', resource=url, scan=1)
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            result = response.json()
            await ctx.send(f"Вывод json: ```json\n{json.dumps(result['permalink'], sort_keys=False, indent=4)}```")
            print(len(json.dumps(result['permalink'], sort_keys=False, indent=4)))


def setup(bot):
    bot.add_cog(Virustotal(bot))
