import discord
import random
from config import config
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['kubik', 'r', 'рандом', 'кубик', 'к'], description="Бросить кубик", usage="<Аргумент от 1 до сколько хотите>")
    async def random(self, ctx, arg1: int):
        if arg1 <= 0:
            await ctx.reply("Меньше 0 нельзя!")
        elif not arg1:
            await ctx.reply("Введи число!")
        else:
            a = random.randint(1, int(arg1))
            embed = discord.Embed(title = "кубик", description=f"У вас: {arg1}, а у меня: {a}", colour = discord.Colour.green())
            embed.set_footer(text=f"©️ strannikbot все права защищены")
            await ctx.reply(embed=embed)

    @commands.command()
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
            await ctx.reply(file=discord.File(fp=image_pix, filename='pix_ava.png'))
        else:
            await ctx.reply("вы не ввели текст!")
def setup(bot):
    bot.add_cog(Fun(bot))