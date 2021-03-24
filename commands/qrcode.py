import discord
from discord.ext import commands
import qrcode
import io
from io import BytesIO

class Qrcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['qr-code', 'кр-код', 'гр-код'])
    async def qrcode(self, ctx, *, arg=None):
        if arg is None:
            embed = discord.Embed(title='Ошибка', description=f'Укажите текст `s.qr-code <text>`', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            img = qrcode.make(arg)
            output = BytesIO()
            img.save(output, 'png')
            image_pix=BytesIO(output.getvalue())
            embed = discord.Embed(title="qr-code", description=f"Текст: {arg}", colour=discord.Colour.gold())
            embed.set_footer(text="©️ strannikbot все права защищены")
            #embed.set_image(url=image_pix)
            await ctx.reply(embed=embed)
            msg = await ctx.send(file=discord.File(fp=image_pix, filename="qrcode.png"))
            await msg.add_reaction("🗑️")
            reaction, user = await self.bot.wait_for("reaction_add",check=lambda reaction,user: user.id == ctx.author.id and str(reaction.emoji) in ["🗑️"] and reaction.message.id == msg.id)
            if str(reaction.emoji) == "🗑️":
                #idea_channel = self.bot.get_channel()
                await msg.clear_reactions()
                await ctx.message.delete()
            else:
                return False

def setup(bot):
    bot.add_cog(Qrcode(bot))