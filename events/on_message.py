import discord
from discord.ext import commands

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        bad_words = "сука" 
        bad_words2 = "с2ka" 
        bad_words3 = "бля"
        bad_words4 = "blya" 
        bad_words5 = "бл4" 
        bad_words6 = "пиздец"
        bad_words7 = "пизд5ц"
        bad_words8 = "хуй"
        bad_words9 = "х7й"
        bad_words10 = "блять"
        bad_words11 = "бл2ть"

        msg = message.content.lower()

        if msg.find(bad_words) != -1 or msg.find(bad_words2) != -1 or msg.find(bad_words3) != -1 or msg.find(bad_words4) != -1 or msg.find(bad_words5) != -1 or msg.find(bad_words6) != -1 or msg.find(bad_words7) != -1 or msg.find(bad_words8) != -1 or msg.find(bad_words9) != -1 or msg.find(bad_words10) != -1 or msg.find(bad_words11) != -1:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Не матерись!")

def setup(bot):
    bot.add_cog(Message(bot))