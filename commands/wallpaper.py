import time
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

class Wallpapers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.domain = "http://getwallpapers.com"
    
    @commands.command()
    async def wallpaper(self, ctx):
        responce = requests.get("http://getwallpapers.com/collection/flat-wallpaper-hd").text
        all_block = BeautifulSoup(responce, "lxml").find_all("div", class_="flexbox_item")
        image_url = ""
        a = 0
        for image in all_block:
            image_url = image.get("data-fullimg")
            if image_url:
                result = self.domain + str(image_url)
                embed = discord.Embed(title="Обои", description=f"[тык]({result})")
                embed.set_image(url=result)
                await ctx.send(embed=embed)
                time.sleep(10)

def setup(bot):
    bot.add_cog(Wallpapers(bot))