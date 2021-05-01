import discord
import random
import nekos
from discord.ext import commands

nekos1 = ['feet',
          'yuri',
          'trap',
          'futanari',
          'hololewd',
          'lewdkemo',
          'solog',
          'feetg',
          'erokemo',
          'les',
          'lewdk',
          'tickle',
          'lewd',
          'feed',
          'eroyuri',
          'eron',
          'cum_jpg',
          'bj',
          'nsfw_neko_gif',
          'solo',
          'kemonomimi',
          'gasm',
          'anal',
          'hentai',
          'erofeet',
          'holo',
          'blowjob',
          'pussy',
          'holoero',
          'lizard',
          'pussy_jpg',
          'pwankg',
          'kuni',
          'waifu',
          'pat',
          'kiss',
          'femdom',
          'spank',
          'cuddle',
          'erok',
          'boobs',
          'random_hentai_gif',
          'ero',
          'goose']


class NSFW(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hentai(self, ctx):
        import aiontai

        api = aiontai.API()

        doujin = await api.get_doujin(1)
        pages = ""
        for page in doujin:
            pages += page.url
            return
        print(pages)
        embed = discord.Embed(title="hentai")
        embed.set_image(url=pages)
        await ctx.send(embed=embed)

    @commands.command(aliases=['n'])
    async def nekos(self, ctx, arg=None):
        await ctx.message.delete()

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:

            a = nekos.img(random.choice(nekos1))
            if arg is None:
                emb = discord.Embed(title=':flushed: NSFW', url=a)
                emb.set_image(url=a)
                emb.set_footer(text='Если не работает, тыкай NSFW!')
                await ctx.send(embed=emb)
                # await ctx.send(random_post.url)

                return

            a = nekos.img(random.choice(nekos1))
            emb = discord.Embed(title=':flushed: NSFW', url=a)
            emb.set_image(url=a)
            emb.set_footer(text='Если не работает, тыкай NSFW!')
            await ctx.send(embed=emb)
            # await ctx.send(random_post.url)
        else:
            if ctx.message.channel.id == 828229933359956008 and ctx.guild.id == 827838959006253068:
                a = nekos.img(random.choice(nekos1))
                emb = discord.Embed(title=':flushed: NSFW', url=a)
                emb.set_image(url=a)
                emb.set_footer(text='Если не работает, тыкай NSFW!')
                await ctx.send(embed=emb)
                # await ctx.send(random_post.url)

                return
            emb = discord.Embed(title=':flushed: Ты не можешь использовать эту команду здесь!')
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(NSFW(client))
