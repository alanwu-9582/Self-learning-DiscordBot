import discord
from discord.ext import commands

import requests
import twstock # 台灣證券交易所

class Economic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_company_code(self, company_name):
        codes = twstock.codes
        for code, name in codes.items():
            if company_name in name:
                return code

        return None

    @commands.command(name="economic", aliases=["stock"], help="查詢台灣股票")
    async def _economic(self, ctx, company_name):
        try:
            stock_id = int(company_name)

        except:
            stock_id = self.get_company_code(company_name)

        try:
            if stock_id == None:
                await ctx.send(f"找不到 {company_name} 的資訊 (?")

            else:
                data_url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
                info_url = f"https://www.twse.com.tw/zh/listed/profile/company.html?{stock_id}"
                response = requests.get(data_url)
                data = response.json()

                if "msgArray" in data:
                    msg = data["msgArray"][0]
                    name = msg["n"]
                    name_full = msg["nf"]
                    now_price = float(msg["z"])
                    last_price = float(msg["y"])
                    data_date = msg["d"]
                    embed=discord.Embed(
                        title=f"{name} ({stock_id})", 
                        url=f"{info_url}", 
                        description=f"{name_full}", 
                        color=[0x2cc32d, 0xe52822][now_price-last_price >= 0]
                    )
                    embed.add_field(name="資料日期", value=f"{data_date}", inline=True)
                    embed.add_field(name="目前股價", value=f"{now_price}", inline=True)
                    embed.add_field(name="漲跌", value=f"{round(now_price-last_price, 2)}", inline=True)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("無法獲取股票資訊")

        except Exception as exception:
            await ctx.send(f"錯誤._. `{exception}`")

async def setup(bot):
    await bot.add_cog(Economic(bot))