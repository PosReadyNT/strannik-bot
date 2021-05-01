import discord
import random
from config import config
from discord.ext import commands
import io
import os
from discord_slash import SlashCommand, cog_ext
from simpledemotivators import demcreate
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="random", description="Бросить кубик")
    async def random(self, ctx, arg1: int):
        if arg1 <= 0:
            await ctx.send("Меньше 0 нельзя!")
        elif not arg1:
            await ctx.send("Введи число!")
        else:
            a = random.randint(1, int(arg1))
            embed = discord.Embed(title = "кубик", description=f"У вас: {arg1}, а у меня: {a}", colour = discord.Colour.green())
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.send(embed=embed)

    @commands.command(name="dem", description="Сделать демовитатор")
    async def dem(self, ctx, text1: str = None, text2: str = None):
        files = []
        for file in ctx.message.attachments:
            fp = io.BytesIO()
            await file.save(fp = 'kek.jpg')
        dem = demcreate(f'{text1}', f'{text2}')
        dem.makeImage('kek.jpg')
        await ctx.reply(file = discord.File(fp='demresult.jpg'))
        os.system(f'del {self.cwd[:-8]}\\kek.jpg')

    @commands.command(name="cyberpunk", description="Написать текст в картинке киберпанка")
    async def cyberpunk(self, ctx, *, arg):
        if arg != '':
            def cyberp(x):
                global img
                img = Image.open('photo.png')
                font = ImageFont.truetype('BlenderPro-Book.ttf', 35)
                text = ImageDraw.Draw(img)
                pos = [150, 225]
                userText = x
                userText = userText.replace("\\n", "\n")
                userText = userText.replace("\\t", "\t")
                value = 0
                for i in userText:
                    text.text((pos[0], pos[1]), i, font=font, fill=('#000000'))
                    pos[0] += 20
                    value += 1
                    if value == 85:
                        pos[0] = 150
                        pos[1] += 50
                        value = 0
                pos[0] = 150
                pos[1] += 50
            cyberp(arg)
            output = BytesIO()
            img.save(output, 'png')
            image_pix=BytesIO(output.getvalue())
            await ctx.send(file=discord.File(fp=image_pix, filename='pix_ava.png'))
        else:
            await ctx.send(content="вы не ввели текст!")

def setup(bot):
    bot.add_cog(Fun(bot))