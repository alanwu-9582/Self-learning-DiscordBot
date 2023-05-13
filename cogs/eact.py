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

    @commands.command(name="ping", help="顯示延遲")
    async def ping(self, ctx):
        colors = [hex(random.randint(16, 255))[2:] for i in range(3)]
        embed=discord.Embed(color=eval("0x"+"".join(colors)))
        embed.add_field(name="Pong!", value="📶 延遲 : %.2f ms" %(self.bot.latency * 1000), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="vote", help="建立投票 <問題> <選項1> <選項2>")
    async def vote(self, ctx, question, *options):
        if len(options) <= 1:
            await ctx.send("至少需要提供2個選項！")
            return

        if len(options) > 10:
            await ctx.send("最多只能提供10個選項！")
            return

        color = "".join([hex(random.randint(1, 255))[2:] for i in range(3)])
        embed = discord.Embed(title=f"**投票：{question}**", description="請投票", color=eval("0x" + color))

        reactions = []
        for i in range(len(options)):
            reactions.append(chr(0x1f1e6 + i))
            embed.add_field(name=f"{chr(0x1f1e6 + i)} {options[i]}", value="\u200b", inline=False)

        message = await ctx.send(embed=embed)
        for reaction in reactions:
            await message.add_reaction(reaction)

async def setup(bot):
    await bot.add_cog(React(bot))