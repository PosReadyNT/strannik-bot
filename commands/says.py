from discord.ext import commands


class Says(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tux-say", description="Говорящий пингвин", usage="s.tux-say <текст>")
    async def p_say(self, ctx, *, arg):
        def isd():
            desc = ""
            a = len(arg)
            for i in range(a):
                desc += "_"
            return desc

        def ids2():
            desc2 = ""
            b = len(arg)
            for i in range(b):
                desc2 += "-"
            return desc2

        def ids3():
            desc3 = ""
            c = len(arg)
            for i in range(c):
                desc3 += " "
            return desc3

        await ctx.send(f"""
```
  {isd()}
< {''.join(arg)} >
  {ids2()}
{ids3()}o
{ids3()} o
{ids3()}    .--.
{ids3()}   |o_o |
{ids3()}   |:_/ |
{ids3()}  //   \ \\
{ids3()} (|     | )
{ids3()}/'\_   _/`\\
{ids3()}\___)=(___/
```
        """)


def setup(bot):
    bot.add_cog(Says(bot))
