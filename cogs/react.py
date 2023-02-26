import discord
from discord.ext import commands

class react(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="echo", help="覆誦訊息")
    async def echo(self, ctx, *,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(name="clean", aliases=['clear'], help="清理訊息")
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)

async def setup(bot):
    await bot.add_cog(react(bot))