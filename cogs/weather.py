import discord
import math
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import os

WEATHER_CHANNEL = 1099314909730312212
DAILY_TIMES = (6, 0)
URL = os.environ.get('WEATHER_API_URL')

class Weather(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.daily_weather, 'cron', hour=DAILY_TIMES[0], minute=DAILY_TIMES[1])

    @commands.Cog.listener()
    async def on_ready(self):
        self.scheduler.start()

    def cog_load(self):
        if self.bot.is_ready():
            self.scheduler.start()

    def cog_unload(self):
        self.scheduler.shutdown()

    async def daily_weather(self):
        channel = self.bot.get_channel(WEATHER_CHANNEL)
        await channel.send("早安啊~ 現在是早上 6:00，以下是今天的天氣預報")
        weather_parameter = self.get_weather_parameter("新北市", 12)
        await channel.send(embed=weather_parameter[0])
        if int(weather_parameter[1][4]) >= 50:
            await channel.send("今天可能會下雨，記得帶傘哇~")

    def get_weather_parameter(self, location_input="新北市", time=24):
        location_input = location_input.replace("台", "臺")
        data = requests.get(URL)
        data_json = data.json()
        result = data_json['records']['location']
        loacation_id = next((i for i, r in enumerate(result) if r["locationName"] == location_input), 1)
        time_index = [int(math.floor(time / 9)), 1][time >= 36 or time <= 0]
        loacation = result[loacation_id]["weatherElement"]
        weatherElements = [loacation[i]["time"][time_index]["parameter"]["parameterName"] for i in range(5)]
        embed=discord.Embed(title="一般天氣預報-今明36小時天氣預報", description=f"{location_input}未來{time}小時天氣預報", color=0x85d6ff)
        embed.add_field(name="天氣現象", value=f"{weatherElements[0]}", inline=False)
        embed.add_field(name="氣溫", value=f"{weatherElements[2]}~{weatherElements[4]}°C", inline=False)
        embed.add_field(name="舒適度", value=f"{weatherElements[3]}", inline=False)
        embed.add_field(name="降雨機率", value=f"{weatherElements[1]}%", inline=False)
        embed.set_footer(text=f'時間區段:{loacation[0]["time"][time_index]["startTime"]} ~ {loacation[0]["time"][time_index]["endTime"]}')
        return embed, weatherElements

    @commands.command(name="weather", help="查尋天氣預報 (地區, 時間)")
    async def get_weather(self, ctx, location_input="新北市", time=24):
        weather_parameter = self.get_weather_parameter(location_input, time)
        await ctx.send(embed=weather_parameter[0])

async def setup(bot):
    await bot.add_cog(Weather(bot))
