import discord
from discord.ext import commands

import requests
def get_key(dict, val):
    for key, value in dict.items():
        if val == value:
            return key
 
    return "未知"

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-BBF22EAE-9D45-465B-BDDF-924B91148BA7&format=JSON'

def get_parameter(result, location_id, loacationN, weather_name, weather_id, weatherE):
    parameter = result[location_id[loacationN]]["weatherElement"][weather_id[weatherE]]["time"][2]["parameter"]
    parameter_name = parameter["parameterName"]

    if weatherE.endswith("T"):
        parameter_name += "∘" + parameter["parameterUnit"]

    elif weatherE == "PoP":
        parameter_name += "%"

    return f"**{loacationN}**未來 24 小時的**{get_key(weather_name, weatherE)}**是**{parameter_name}**"

def get_weather(loacationN="新北市", weatherE="all"):
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
        return "找不到這個地區"
    
    if weatherE == "all":
        output = ""
        for wE in list(weather_name.values()):
            output += f"{get_parameter(result, location_id, loacationN, weather_name, weather_id, wE)}\n"

        return output   

    else:
        if weatherE not in weather_id:
            if weatherE not in weather_name:
                return "找不到這個預報因子"

            else:
                weatherE = weather_name[weatherE]

        return get_parameter(result, location_id, loacationN, weather_name, weather_id, weatherE)

class web_crawler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="weather", help="查尋天氣預報")
    async def weather(self, ctx, loacationN="新北市", weatherE="all"):
        await ctx.send(get_weather(loacationN, weatherE))

async def setup(bot):
    await bot.add_cog(web_crawler(bot))

