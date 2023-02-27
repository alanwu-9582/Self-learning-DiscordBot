import discord
from discord.ext import commands

from time import *
from math import *
from random import *

def QradEqua(a: int, b: int, c: int): #一元二次方程式
    Discriminant = pow(b, 2) - (4 * a * c)
    if Discriminant < 0:
        return "No solution"

    elif Discriminant == 0:
        return f"{(-b + pow(Discriminant, 0.5)) / 2 * a}"

    else:
        return f"{(-b - pow(Discriminant, 0.5)) / 2 * a}, {(-b + pow(Discriminant, 0.5)) / 2 * a}"

class calculate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(neme="calculate", aliases=["compute"], help="表達式運算")
    async def calculate(self, ctx, *,arg):
        try:
            ans = eval(arg)
            await ctx.send(f"`{arg} = {ans}`")

        except Exception as e:
            await ctx.send(f"好難喔我不會ㄟ\n`{e}`")

async def setup(bot):
    await bot.add_cog(calculate(bot))