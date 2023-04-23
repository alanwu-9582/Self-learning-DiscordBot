import discord
import math
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import os

def get_key(dict, val):
    for key, value in dict.items():
        if val == value:
            return key
 
    return "未知"

def get_parameter(result, location_info, weather_info, weatherE, time):

    location_id, loacationN = location_info
    weather_name, weather_id = weather_info

    time_index = int(math.floor(time / 9))
    parameter = result[location_id[loacationN]]["weatherElement"][weather_id[weatherE]]["time"][time_index]["parameter"]
    parameter_name = parameter["parameterName"]

    if weatherE.endswith("T"):
        parameter_name += "∘" + parameter["parameterUnit"]

    elif weatherE == "PoP":
        parameter_name += "%"

    return f"**{loacationN}**未來 **{time}** 小時的**{get_key(weather_name, weatherE)}**是**{parameter_name}**", parameter["parameterName"]

def get_weather(loacationN="新北市", weatherE="all", time=24):

    data = requests.get(url)
    data_json = data.json()
    result = data_json['records']['location']

    location_id = {}
    weather_id = {}
    weather_name = {"天氣現象": "Wx", "最高溫度": "MaxT", "最低溫度": "MinT", "舒適度": "CI", "降雨機率": "PoP"}

    if "台" in loacationN:
        loacationN = loacationN.replace("台", "臺")

    for i in range(len(result)):
        location_id[result[i]["locationName"]] = i

        if i == 0:
            for j in range(len(result[i]["weatherElement"])):
                weather_id[result[i]["weatherElement"][j]["elementName"]] = j


    if loacationN not in location_id:
        loacationN = "新北市"

    if weatherE not in weather_id:
            if weatherE not in weather_name:
                weatherE="all"

            else:
                weatherE = weather_name[weatherE]
    
    if time <= 0 or time >= 36:
        time = 24  

    location_info = [location_id, loacationN]
    weather_info = [weather_name, weather_id]
    
    if weatherE == "all":
        output = ""
        output_weather = []
        for wE in list(weather_name.values()):
            weather_results = get_parameter(result, location_info, weather_info, wE, time)
            output += f"{weather_results[0]}\n"
            output_weather.append(weather_results[1])

        return output, output_weather

    else:
        return get_parameter(result, location_info, weather_info, weatherE, time)

WEATHER_CHANNEL = 1099314909730312212
url = os.environ['WEATHER_API_URL']
daily_times = [6, 0]

class weather(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.daily_weather, 'cron', hour=daily_times[0], minute=daily_times[1])

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
        parameter_result = get_weather("新北市", "all", 12)
        await channel.send(parameter_result[0])
        
        if int(parameter_result[1][4]) >= 50:
            await channel.send("今天可能會下雨，記得帶傘喔")
        
    @commands.command(name="weather", help="查尋天氣預報 (地區, 預報因子, 時間)")
    async def _weather(self, ctx, loacationN="新北市", weatherE="all", time=24):
        await ctx.send(get_weather(loacationN, weatherE, time)[0])

    @commands.command(name="parameter", aliases=["get_parameter"], help="顯示預報因子")
    async def _parameter(self, ctx, loacationN="新北市", weatherE="all", time=24):
        await ctx.send("`Wx 天氣現象, MaxT 最高氣溫, MinT 最低氣溫, CI 舒適度, PoP 降雨機率`")

async def setup(bot):
    await bot.add_cog(weather(bot))