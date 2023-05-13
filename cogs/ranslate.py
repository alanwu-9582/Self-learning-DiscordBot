import discord
from discord.ext import commands

import googletrans
translator = googletrans.Translator()

class Traslate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="translate", help="翻譯 (翻譯成的語言, 內容)")
    async def traslate(self, ctx, dest_lang, *,arg: str):
        if dest_lang in googletrans.LANGCODES:
            dest_lang = googletrans.LANGCODES[dest_lang]
        
        if dest_lang in googletrans.LANGUAGES:
            translations = translator.translate(arg, dest=dest_lang)
            await ctx.send(translations.text)

        else:
            await ctx.send(f"找不到 `{dest_lang}`")

    @commands.command(name="langcodes", help="查看語言編碼")
    async def langcodes(self, ctx, *,languages=None):
        if languages == None:
            await ctx.send(f"以下是可翻譯的語言編碼\n語言編碼: `{googletrans.LANGCODES}`")

        elif languages in googletrans.LANGCODES:
            await ctx.send(f"`{languages}` 的語言編碼是 `{googletrans.LANGCODES[languages]}`")

        elif languages in googletrans.LANGUAGES:
            await ctx.send(f"`{languages}` 的語言是 `{googletrans.LANGUAGES[languages]}`")

        else:
            await ctx.send(f"找不到 `{languages}`")
    
    @commands.command(name="detect", help="偵測語言")
    async def detect_lang(self, ctx, *,arg):
        m_lang = translator.detect(arg)
        await ctx.send(f"{arg} 有 `{round(m_lang.confidence*100, 2)}%` 的機率是 `{googletrans.LANGUAGES[m_lang.lang]}`, 語言編碼: `{m_lang.lang}`")

async def setup(bot):
    await bot.add_cog(Traslate(bot))