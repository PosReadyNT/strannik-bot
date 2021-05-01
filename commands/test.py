import discord
import aiohttp
import requests
import random
import datetime
from bs4 import BeautifulSoup
import ast
import asyncio
from discord.ext import commands


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        counter = 0
        async for _ in ctx.channel.history(limit=None):
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

    @commands.command(aliases=['ev', 'e'])
    async def eval_fn(self, ctx, *, cmd):
        if ctx.author.id == 694598900094599198:
            def insert_returns(badi):
                if isinstance(badi[-1], ast.Expr):
                    badi[-1] = ast.Return(badi[-1].value)
                    ast.fix_missing_locations(badi[-1])

                if isinstance(badi[-1], ast.If):
                    insert_returns(badi[-1].body)
                    insert_returns(badi[-1].orelse)

                if isinstance(badi[-1], ast.With):
                    insert_returns(badi[-1].body)

            fn_name = "_eval_expr"

            cmd = cmd.strip("` ")

            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

            body = f"async def {fn_name}():\n{cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                'guild': ctx.guild,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            await ctx.send(await eval(f"{fn_name}()", env))
        else:
            await ctx.send("Пшиф отсюда! Я повинуюсь только своему создателю!")

    @commands.command()
    async def google(self, ctx, *, question=None):
        if question is None:
            await ctx.send('Введите запрос!')
        else:
            await ctx.send('Подождите!')

            url = f'https://www.google.com/search?b-d&q=' + str(question).replace(' ', '+')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
            }

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            items = soup.findAll('div', class_="rc")

            comps = []

            for item in items:
                comps.append({
                    'link': item.find('a').get('href'),
                    'title': item.find('h3', class_='LC20lb DKV0Md').get_text(strip=True)
                })
                await asyncio.sleep(3)

            emb = discord.Embed()

            counter = 0
            for comp in comps:
                counter += 1

                emb.add_field(
                    name=f'[{counter}]    > #' + comp['title'],
                    value='| ' + comp['link'],
                    inline=False
                )

            emb.set_author(name='{}'.format(ctx.author), icon_url='{}'.format(ctx.author.avatar_url))
            await ctx.send(embed=emb)

    @commands.command()
    async def переводчик_3(self, ctx, *, message=None):
        a = {"q": "й",
             "w": "ц",
             "e": "у",
             "r": "к",
             "t": "е",
             "y": "н",
             "u": "г",
             "i": "ш",
             "o": "щ",
             "p": "з",
             "[": "х",
             "{": "х",
             "}": "ъ",
             "]": "ъ",
             "a": "ф",
             "s": "ы",
             "d": "в",
             "f": "а",
             "g": "п",
             "h": "р",
             "j": "о",
             "k": "л",
             "l": "д",
             ":": "ж",
             ";": "ж",
             '"': "э",
             "'": "э",
             "z": "я",
             "x": "ч",
             "c": "с",
             "v": "м",
             "b": "и",
             "n": "т",
             "m": "ь",
             "<": "б",
             ",": "б",
             ">": "ю",
             ".": "ю",
             "?": ",",
             "/": ".",
             "`": "ё",
             "~": "ё",
             " ": " "}
        global errors_itog
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
                    errors_itog = ""
                else:
                    errors_itog = f"\nНепереведенные символы: {errors}"

            if len(itog) <= 0:
                print("Перевода нет!")
            else:
                itog_new = f"Перевод: {itog}"
                await ctx.send(f"{itog_new}")

    @commands.command()
    # @commands.has_role()
    async def g(self, ctx, mins: int, *, prize: str):
        embed = discord.Embed(title="Розыгрыш!", description=f"{prize}", color=ctx.author.color)

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=mins * 60)

        embed.add_field(name="Заканчивается в:", value=f"{end[:19]} UTC")
        embed.set_footer(text=f"Заканчивается через {mins} минут с данного времени!")

        my_msg = await ctx.send(embed=embed)

        await my_msg.add_reaction("🎉")

        await asyncio.sleep(mins * 60)

        new_msg = await ctx.channel.fetch_message(my_msg.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await ctx.send(f"Поздравления! {winner.mention} выиграл {prize}!")


def setup(bot):
    bot.add_cog(Testing(bot))
