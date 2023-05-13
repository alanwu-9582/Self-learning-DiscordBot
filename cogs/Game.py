import discord
from discord.ext import commands

import random

class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nowPlaying = None

    def calculate_a_b(self, guess, ans): # for 1a2b
        count_a = 0
        count_b = 0

        for i in range(len(guess)):
            if guess[i] in ans: # 第 i 個字元是否在 ans 中
                if guess[i] == ans[i]: # 位置相同
                    count_a += 1
                else:
                    count_b += 1

        return count_a, count_b

    @commands.command(name="gameStop", help="結束遊戲")
    async def stopPlaying(self, ctx, guess=None):
        await ctx.send(f"結束正在遊玩的 {self.nowPlaying}")
        self.nowPlaying = None


    @commands.command(name="roll", aliases=['dice'], help="擲骰子 <次數> <骰子面數> <成功條件>")
    async def dice(self, ctx, times: int, faces: int, *,success=None):
        dices = [random.randint(1, faces) for i in range(times)]

        await ctx.send(", ".join(list(map(str, dices))))
        if success != None:
            try:
                await ctx.send(f"成功了 {len(list(filter(lambda point: eval(str(point)+success), dices)))} 次")
            except Exception as exception:
                await ctx.send(f"成功的條件怪怪的.. `{exception}`")

    @commands.command(name="oatb", aliases=['1a2b'], help="遊玩1a2b <四位數字(不重複, 沒有0)>")
    async def oatb(self, ctx, guess=None):
        n = 4
        if self.nowPlaying == "1a2b":
            if guess is not None:
                a, b = self.calculate_a_b(guess, self.ans)
                if a == n:
                    await ctx.send(f"<@{ctx.author.id}> 猜對了!!") 
                    self.nowPlaying = None
                else:
                    await ctx.send(f"{a}A{b}B")
            else:
                await ctx.send("請猜一個四位數字(不重複, 沒有0)")

        elif self.nowPlaying is None:
            self.nowPlaying = "1a2b"
            await ctx.send(f"<@{ctx.author.id}> 開始了一個 1a2b 的遊戲")
            self.ans = ''.join(random.sample('123456789', n))
            print(self.ans)

        else:
            await ctx.send(f"目前正在遊玩 {self.nowPlaying} 請先結束\n可以使用 `gameStop 結束`")

async def setup(bot):
    await bot.add_cog(Game(bot))