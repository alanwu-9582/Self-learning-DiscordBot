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

class Recursion(): #遞迴
    def __init__(self, a1: int, relation: str):
        self.a1 = a1
        self.relation = relation
        self.sequence = []

    def get_n(self, an):
        a = [0] + [self.a1 for n in range(an)]
        for n in range(2, an + 1):
            a[n] = eval(self.relation)

        self.sequence = a
        return a[an]

    def get_sequence(self, n):
        self.get_n(n)
        return self.sequence

def sigma(k: int, m_n: int, relation: str): #累加
    array = [0] + [0 for i in range(m_n)]
    for n in range(k, m_n+1):
        array[n] = eval(relation)
        
    return sum(array)

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