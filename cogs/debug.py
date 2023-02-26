import discord
from discord.ext import commands

class debug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping", help="顯示延遲")
    async def ping(self, ctx):
        embed=discord.Embed(color=0xec659f)
        embed.add_field(name="Pong!", value="📶 延遲 : %.2f ms" %(self.bot.latency * 1000), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(debug(bot))