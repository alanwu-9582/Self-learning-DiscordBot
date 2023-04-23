import discord
from discord.ext import commands

import random

WELCOME_CHANNEL = 1007909237982244865

AFFIXS = [
    ["歡迎 ", "。打聲招呼吧！"], 
    ["耶，您成功了，", ""], 
    ["", " 剛剛滑入了伺服器中。"], 
    ["野生的 ", " 出現。"], 
    ["歡迎，", "。 我們希望您帶個披薩來。"], 
    ["大家一起歡迎 ", ""], 
    ["", "滑進了蘿莉中"]
    ]

class event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        affix = random.randint(0, len(AFFIXS)-1)
        channel = self.bot.get_channel(WELCOME_CHANNEL)
        await channel.send(f"{AFFIXS[affix][0]}<@{member.id}>{AFFIXS[affix][1]}")

    @commands.Cog.listener()
    async def on_message(self, msg):
        pass

async def setup(bot):
    await bot.add_cog(event(bot))