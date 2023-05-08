import discord
from discord.ext import commands

import sqlite3

DATABASE = "RuruhimeLearningData.db" 
TABLE = "LearningData"

class Learning(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.conn = sqlite3.connect(DATABASE)
        self.m_cursor = self.conn.cursor()

        self.m_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE} (
            keyword text NOT NULL,
            response text NOT NULL
        );''')
        self.conn.commit()
    
    def cog_unload(self):
        self.m_cursor.close()
        self.conn.close()

    def get_data(self, arg):
        self.m_cursor.execute(f"SELECT * FROM {TABLE} WHERE keyword=?;", (arg,))
        return self.m_cursor.fetchone()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author != self.bot.user:
            data = self.get_data(msg.content)
            if data != None:
                await msg.channel.send(data[1])

    @commands.command(name="learn", help="讓綸綸姬學點東西(關鍵字, 回覆)")
    async def learn(self, ctx, keyword, *,response):
        if self.get_data(keyword) == None:
            self.m_cursor.execute(f"INSERT INTO {TABLE} VALUES ('{keyword}', '{response}');")
        
        else:
            self.m_cursor.execute(f"UPDATE {TABLE} SET response = '{response}' WHERE keyword = '{keyword}'")

        self.conn.commit()
        await ctx.send("好哇! 我學起來ㄌ~")

    @commands.command(name="forget", help="讓綸綸姬忘掉學的點東西(關鍵字)")
    async def forget(self, ctx, keyword):
        data = self.get_data(keyword)
        if data == None:
            await ctx.send("我沒學過這個 :(")
        
        else:
            self.m_cursor.execute(f"DELETE from {TABLE} WHERE keyword = '{keyword}';")
            self.conn.commit()
            await ctx.send(f"我剛剛把 `{data}` 忘記了 :P")

async def setup(bot):
    await bot.add_cog(Learning(bot))