import discord
import aiohttp
import requests
import random
import datetime
from bs4 import BeautifulSoup
import asyncio
from PIL import Image
from io import BytesIO
from discord.ext import commands

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        counter = 0
        async for message in ctx.channel.history(limit=None):
            counter += 1
        counter += 3
        await ctx.send(f"msg: {counter}")

    @commands.command()
    @commands.is_owner()
    async def meme(self, ctx):
        embed = discord.Embed(title="test", description="test")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/meme') as r:
                res = await r.json()
                embed.set_image(url=res['image'])
                await ctx.send(embed=embed)
    
    @commands.command()
    async def giveaway(self, ctx,channel: discord.TextChannel, seconds: int, *, args):
        msg = await ctx.send(args)
        await msg.add_reaction("🎂")
        asyncio.sleep(seconds)
        member = ctx.author.id
        chan = channel.id
        win = await self.bot.get_channel(chan).fetch_message(msg)
        import random
        await ctx.send(f"winner: {random.choice(win)}")

    @commands.command()
    async def google(self, ctx, *, question = None):
        if question is None:
            await ctx.send('Введите запрос!')
        else:
            await ctx.send('Подождите!')

            url = f'https://www.google.com/search?b-d&q=' + str(question).replace(' ', '+')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
            }

            r = requests.get(url, headers = headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            items = soup.findAll('div', class_ = "rc")

            comps = []

            for item in items:
                comps.append({
                        'link': item.find('a').get('href'),
                        'title': item.find('h3', class_ = 'LC20lb DKV0Md').get_text(strip = True)
                    })
                await asyncio.sleep(3)

            emb = discord.Embed()
            
            counter = 0
            for comp in comps:
                counter += 1

                emb.add_field(
                        name = f'[{counter}]    > #'  + comp['title'],
                        value =  '| ' + comp['link'],
                        inline = False
                    )


            emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))
            await ctx.send(embed = emb)

            
    @commands.command()
    async def переводчик_3(self, ctx,*,message=None):
        a = {"q":"й","w":"ц","e":"у","r":"к","t":"е","y":"н","u":"г","i":"ш","o":"щ","p":"з","[":"х","{":"х","}":"ъ","]":"ъ","a":"ф","s":"ы","d":"в","f":"а","g":"п","h":"р","j":"о","k":"л","l":"д",":":"ж",";":"ж",'"':"э","'":"э","z":"я","x":"ч","c":"с","v":"м","b":"и","n":"т","m":"ь","<":"б",",":"б",">":"ю",".":"ю","?":",","/":".","`":"ё","~":"ё"," ":" "}
        if message is None:
            await ctx.send("Введи символ")
        else:
            itog = ""
            errors = ""
            for i in message:
                if i.lower() in a:
                    itog += a[i.lower()]
                else:
                    errors += f"`{i}` "
                if len(errors) <= 0:
                    errors_itog=""
                else:
                    errors_itog=f"\nНепереведенные символы: {errors}"

            if len(itog) <= 0:
                itog_new= "Перевода нет!"
            else:
                itog_new=f"Перевод: {itog}"
                await ctx.send(f"{itog_new}{errors_itog}")

    @commands.command()
    #@commands.has_role()
    async def g(self, ctx, mins : int, * , prize: str):
        embed = discord.Embed(title = "Розыгрыш!", description = f"{prize}", color = ctx.author.color)

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

        embed.add_field(name = "Заканчивается в:", value = f"{end[:19]} UTC")
        embed.set_footer(text = f"Заканчивается через {mins} минут с данного времени!")

        my_msg = await ctx.send(embed = embed)


        await my_msg.add_reaction("🎉")


        await asyncio.sleep(mins*60)


        new_msg = await ctx.channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await ctx.send(f"Поздравления! {winner.mention} выиграл {prize}!")

def setup(bot):
    bot.add_cog(Testing(bot))