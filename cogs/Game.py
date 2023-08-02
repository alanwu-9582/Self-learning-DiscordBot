import discord
from discord.ext import commands

import random

# for tictactoe
PLAYER_SYMBOLS = ["O", "X"]
WIN_CONDITIONS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]] 

class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nowPlaying = None

    @commands.command(name="gameStop", aliases=['gamestop'], help="結束遊戲")
    async def stopPlaying(self, ctx, guess=None):
        await ctx.send(f"結束正在遊玩的 {self.nowPlaying}")
        self.nowPlaying = None

    @commands.command(name="roll", aliases=['dice'], help="擲骰子 <次數> <骰子面數> <成功條件>")
    async def dice(self, ctx, times: int, faces: int, *,success=None):
        dices = [random.randint(1, faces) for i in range(times)]

        await ctx.send(", ".join(list(map(str, dices))))
        if success != None:
            try:
                await ctx.send(f"成功了 {len(list(filter(lambda point: eval(str(point)+success), dices)))} 次")
            except Exception as exception:
                await ctx.send(f"成功的條件怪怪的.. `{exception}`")

    # 1a2b
    def calculate_a_b(self, guess, ans): 
        count_a = 0
        count_b = 0

        for i in range(len(guess)):
            if guess[i] in ans: 
                if guess[i] == ans[i]: 
                    count_a += 1
                else:
                    count_b += 1

        return count_a, count_b

    @commands.command(name="oatb", aliases=['1a2b'], help="遊玩1a2b <四位數字(不重複, 沒有0)>")
    async def oatb(self, ctx, user_guess=None):
        n = 4
        if self.nowPlaying == "1a2b":
            if user_guess is not None:
                a, b = self.calculate_a_b(user_guess, self.ans)
                if a == n:
                    await ctx.send(f"<@{ctx.author.id}> 猜對了!!") 
                    self.nowPlaying = None
                else:
                    await ctx.send(f"{a}A{b}B")
            else:
                await ctx.send("請猜一個四位數字(不重複, 沒有0)")

        elif self.nowPlaying is None:
            self.nowPlaying = "1a2b"
            await ctx.send(f"<@{ctx.author.id}> 開始了一個 1a2b 的遊戲")
            await ctx.send("請猜一個四位數字(不重複, 沒有0)")
            self.ans = ''.join(random.sample('123456789', n))

        else:
            await ctx.send(f"目前正在遊玩 {self.nowPlaying} 請先結束\n可以使用 `gameStop 結束`")

    # tictactoe
    def output_frame(self):
        temp_frame = []
        for i in range(0, 9, 3):
            temp_frame.append(" | ".join(self.frame[i:i+3]))

        return " \n-------- \n".join(temp_frame)

    def select_grid(self, select_id):
        try:
            select_id = int(select_id)
            if select_id not in range(1, 10):
                return "輸入錯誤"
            if select_id in self.selected:
                return f"第 {select_id} 格已經被選過了"

            self.frame[select_id-1] = PLAYER_SYMBOLS[self.round_count % 2]
            self.round_count += 1
            self.selected.append(select_id)
            return self.output_frame()
        except:
            return "格式錯誤"

    def check_win(self):
        for symbol in PLAYER_SYMBOLS:
            for win_condition in WIN_CONDITIONS:
                if all(self.frame[i] == symbol for i in win_condition):
                    return symbol
        return None

    def get_next_move(self):
        empty_indices = [i for i, x in enumerate(self.frame) if x not in PLAYER_SYMBOLS]
        for i in empty_indices:
            self.frame[i] = PLAYER_SYMBOLS[self.round_count % 2]
            if self.check_win() == PLAYER_SYMBOLS[self.round_count % 2]:
                return i+1
            self.frame[i] = str(i+1)

        for i in empty_indices:
            self.frame[i] = PLAYER_SYMBOLS[(self.round_count+1) % 2]
            if self.check_win() == PLAYER_SYMBOLS[(self.round_count+1) % 2]:
                return i+1
            self.frame[i] = str(i+1)

        count = 1
        while len(empty_indices) > 1 and count < 8 :
            if count in empty_indices:
                empty_indices.remove(count)
            count += 2
        return 5 if 4 in empty_indices else random.choice(empty_indices) + 1

    async def computer_select(self, ctx):
        async with ctx.typing():
            next_move = self.get_next_move()
            await ctx.send(f"綸綸姬選擇了 {next_move} 號格子 <3")
            await ctx.send(self.select_grid(next_move))
            
    @commands.command(name="tictactoe", aliases=['ooxx'], help="遊玩 ooxx")
    async def tictactoe(self, ctx, user_select=None):
        if self.nowPlaying == "ooxx":
            if user_select is not None:
                await ctx.send(self.select_grid(user_select))
                if self.check_win() is not None:
                    await ctx.send(f"玩家獲勝")
                    self.nowPlaying = None
                    return

                elif self.round_count == 9:
                    await ctx.send(f"平手")
                    self.nowPlaying = None
                    return

                if self.round_count % 2 == self.isComputerFirst:
                    await self.computer_select(ctx)
                    if self.check_win() is not None:
                        await ctx.send(f"綸綸姬獲勝")
                        async with ctx.typing():
                            await ctx.send(f"耶~")

                        self.nowPlaying = None
                        return

                    elif self.round_count == 9:
                        await ctx.send(f"平手")
                        self.nowPlaying = None
                        return
            else:
                await ctx.send("請選擇一個格子")

        elif self.nowPlaying is None:
            self.nowPlaying = "ooxx"
            self.frame = [str(i+1) for i in range(9)]
            self.selected = []
            self.round_count = 1
            self.isComputerFirst = random.randint(0, 1)
            
            await ctx.send(f"<@{ctx.author.id}> 開始了一個 ooxx 的遊戲")
            await ctx.send(self.output_frame())
            await ctx.send("綸綸姬先" if self.isComputerFirst else "你先")

            if self.isComputerFirst:
                await self.computer_select(ctx)

        else:
            await ctx.send(f"目前正在遊玩 {self.nowPlaying} 請先結束(可以使用 `gameStop`)")

    @commands.command(name="guessNum", aliases=['guessnum'], help="遊玩猜數字")
    async def guessNum(self, ctx, user_guess=None):
        if self.nowPlaying == "guessNum":
            if user_guess is not None:
                try:
                    user_guess = int(user_guess)
                    if user_guess in range(self.minNum, self.maxNum+1):
                        self.count += 1
                        if user_guess == self.ans:
                            await ctx.send(f"<@{ctx.author.id}> 猜對了!! 猜了{self.count}次")
                            self.nowPlaying = None
                        else:
                            if user_guess < self.ans:
                                await ctx.send(f"太小了~")
                                self.minNum = user_guess

                            elif user_guess > self.ans:
                                await ctx.send(f"太大了~")
                                self.maxNum = user_guess

                            await ctx.send(f"請猜一個`{self.minNum} ~ {self.maxNum}` 的數字")
                    else:
                        await ctx.send(f"超出範圍! \n請猜一個`{self.minNum} ~ {self.maxNum}` 的數字")
                except:
                    await ctx.send(f"格式錯誤 :) \n請猜一個`{self.minNum} ~ {self.maxNum}` 的數字")
            else:
                await ctx.send(f"請輸入數字..")

        elif self.nowPlaying is None:
            self.nowPlaying = "guessNum"

            self.minNum = 1
            self.maxNum = 100
            self.count = 0
            self.ans = random.randint(1, 100)

            await ctx.send(f"<@{ctx.author.id}> 開始了一個 guessNum 的遊戲")
            await ctx.send(f"請猜一個`{self.minNum} ~ {self.maxNum}` 的數字")

        else:
            await ctx.send(f"目前正在遊玩 {self.nowPlaying} 請先結束(可以使用 `gameStop`)")

async def setup(bot):
    await bot.add_cog(Game(bot))