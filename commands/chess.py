import asyncio
import chess
import chess.svg
import discord
from discord_slash import SlashCommand, cog_ext
from discord.ext import commands
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image


class Chess(commands.Cog, name="Chess"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chess-start", description="Запустить шахматы")
    async def start(self, ctx, *, user: discord.User):
        await chess_loop(ctx.author, user, ctx, self.bot)


def setup(bot):
    bot.add_cog(Chess(bot))


async def chess_loop(user1, user2, ctx, bot):
    embed = discord.Embed(title=f"Игра началась!!",
                          description=f"Пишите в мне ЛС для хода шахматы. {user1.mention} - белый, а {user2.mention} чёрный",
                          color=discord.Color.green())
    await ctx.send(embed=embed)
    embed = discord.Embed(title="Как Ходить в шахматах.")
    board = chess.Board()
    img = chess.svg.board(board=board)
    outputfile = open('chess_board.svg', "w")
    outputfile.write(img)
    outputfile.close()
    drawing = svg2rlg("chess_board.svg")
    renderPM.drawToFile(drawing, "chess_board.png", fmt="png")
    img = Image.open('chess_board.png')
    img.save('chess_board.png')
    await ctx.send(file=discord.File(fp="chess_board.png"))
    game_over = False
    while game_over is not True:
        cancel = await board_move(user1, board, ctx, bot)
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            return
        if game_over:
            embed = discord.Embed(title=f"Игра окончена!",
                                  description=f"{user1.mention} выиграл игру!",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            return

        cancel = await board_move(user2, board, ctx, bot)
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            return
        if game_over:
            embed = discord.Embed(title=f"Игра окончена!",
                                  description=f"{user2.mention} Выиграл игру!",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            return


async def board_move(player, board, ctx, bot):
    turn_loop = True
    while turn_loop:
        try:
            message = await bot.wait_for("message", check=lambda m: m.author == player)
        except asyncio.TimeoutError:
            embed = discord.Embed(title=f"Игра остановлена!",
                                  description=f"{ctx.author.mention} долго не писал куда ходить...",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        if message.content.lower() == "cancel":
            embed = discord.Embed(title="Игра окончена",
                                  description=f"{ctx.author.mention} отменил игру.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            delete_array = [message]
            try:
                await ctx.channel.delete_messages(delete_array)
            except Exception as e:
                print(e)
                pass
            return True
        else:
            try:
                split = message.content.split(", ")
                move_from = split[0]
                move_to = split[1]
                joined = "".join(split)
                move = chess.Move.from_uci(joined)
                if move in board.legal_moves:
                    embed = discord.Embed(title=f"Ход",
                                            description=f"{ctx.author.mention} походил с {move_from} в {move_to}!",
                                            color=discord.Color.green())
                    await ctx.send(embed=embed)
                    await player.send(embed=embed)
                    board.push(move)
                    img = chess.svg.board(board=board)
                    outputfile = open('chess_board.svg', "w")
                    outputfile.write(img)
                    outputfile.close()
                    drawing = svg2rlg("chess_board.svg")
                    renderPM.drawToFile(drawing, "chess_board.png", fmt="png")
                    await ctx.send(file=discord.File(fp="chess_board.png"))
                    turn_loop = False
                elif move not in board.legal_moves:
                    embed = discord.Embed(title=f"Ошибка",
                                            description=f"Вы ввели не так ход. Пример: `b2, b4`! "
                                                        f"Попробуйте ещё раз.",
                                            color=discord.Color.red())
                    await ctx.send(embed=embed)
                delete_array = [message]
                await ctx.channel.delete_messages(delete_array)
            except:
                pass