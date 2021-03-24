import discord
from discord.ext import commands
import re
from bs4 import BeautifulSoup
class RateGit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rate_git(self, ctx, *, args):
        import requests
        abc = requests.get(f"https://github-readme-stats.vercel.app/api?username={' '.join(args)}&count_private=true&show_icons=true&theme=algolia").text
        from PIL import Image
        from io import BytesIO

        ios2 = Image.open(abc)
        ios2.save(ios, "PNG")
        await ctx.send(file=discord.File(fp=ios2, filename="test.png"))

    @commands.command()
    async def rate_git2(self, ctx, *, args):
        import shutil

        import requests

        responce = requests.get("https://github-readme-stats.vercel.app/api?username=PosReadyNT&count_private=true&show_icons=true&theme=algolia").content
        soup = BeautifulSoup(responce, 'lxml')
        block = soup.find('rect', id = "card-bg")
        print(block)

    @commands.command()
    async def rate_test(self, ctx, *, args):
        import requests
        import shutil

        image_url = "https://github-readme-stats.vercel.app/username=PosReadyNT&count_private=true&show_icons=true&theme=algolia"
        filename = image_url.split("/")[-1]

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
            print('Image sucessfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retreived')

def setup(bot):
    bot.add_cog(RateGit(bot))