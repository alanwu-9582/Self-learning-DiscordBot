import asyncio
import os

import discord
from discord.ext import commands

import json
with open('./setting.json', 'r', encoding="utf8") as jfile:
  jdata = json.load(jfile)

TOKEN = os.environ['ruruhimetoken']
PREFIX = 'hime.'
STATUS = discord.Status.idle
ACTIVITY = discord.Game(name="蘿莉")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=STATUS, activity=ACTIVITY)
    print(f'>> {bot.user} is online <<<')
  
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"loaded {extension} !!")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"unloaded {extension} !!")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"reloaded {extension} !!")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())