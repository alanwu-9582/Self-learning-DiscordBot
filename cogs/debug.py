import discord
from discord.ext import commands

class debug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping", help="顯示延遲")
    async def ping(self, ctx):
        embed=discord.Embed(color=0xec659f)
        embed.add_fieldd(name="Pong!", value=f"📶 延遲 :{round(self.bot.latency * 1000, 2)} ms" , inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(debug(bot))