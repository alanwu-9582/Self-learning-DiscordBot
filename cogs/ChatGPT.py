import os

import discord
from discord.ext import commands

import openai

import json
with open('./setting.json', 'r', encoding="utf8") as jfile:
  jdata = json.load(jfile)

MODEL_ENGINE = jdata['OPENAI_MODEL_ENGINE']
openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_endpoint = "https://api.openai.com"

class ChatGPT(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="chat", aliases=["openai"],  help="與 ChatGPT 對話")
    async def chat(self, ctx, *,arg):
        user_input = arg

        print(arg)
        try:
            response = openai.Completion.create(
                engine=MODEL_ENGINE,
                prompt=user_input,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7
            )

            await ctx.send(response.choices[0].text)
        except Exception as e:
            print(e)
        

async def setup(bot):
    await bot.add_cog(ChatGPT(bot))