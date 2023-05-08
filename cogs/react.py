import discord
from discord.ext import commands

import random

class React(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="hello", help="Hello")
    async def hello(self, ctx):
        await ctx.send("哈囉! 可以使用 `!help` 獲取更多指令的使用方式哇!ヾ(•ω•`)o")

    @commands.command(name="echo", help="覆誦訊息")
    async def echo(self, ctx, *,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(name="clean", aliases=['clear'], help="清理訊息")
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)

    @commands.command(name="roll", aliases=['dice'], help="擲骰子 <次數> <骰子面數> <成功條件>")
    async def dice(self, ctx, times: int, faces: int, *,success=None):
        dices = [random.randint(1, faces) for i in range(times)]

        await ctx.send(", ".join(list(map(str, dices))))
        if success != None:
            try:
                await ctx.send(f"成功了 {len(list(filter(lambda point: eval(str(point)+success), dices)))} 次")
            except Exception as exception:
                await ctx.send(f"成功的條件怪怪的.. `{exception}`")

    @commands.command(name="ping", help="顯示延遲")
    async def ping(self, ctx):
        colors = [hex(random.randint(16, 255))[2:] for i in range(3)]
        embed=discord.Embed(color=eval("0x"+"".join(colors)))
        embed.add_field(name="Pong!", value="📶 延遲 : %.2f ms" %(self.bot.latency * 1000), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(React(bot))