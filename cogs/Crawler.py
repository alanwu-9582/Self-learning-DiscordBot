import discord
from discord.ext import commands

import instaloader
import os
import shutil

IMAGES_PATH = 'temp'
ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.mp4', '.mkv']

class Crawler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.post_count = 0

    @commands.command(name="instagram", aliases=["ig", "insta"], help="取得 instagram 影像 (無法下載影片..那有點大)")
    async def download_instagram_post(self, ctx, url):
        loader = instaloader.Instaloader(download_videos=False)
        target_path = f'{IMAGES_PATH}{self.post_count}'
        self.post_count += 1
        await ctx.send("開始讀取.. 這可能會需要億點點時間")

        try:
            async with ctx.typing():
                post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
                video_url = post.video_url
                caption = post.caption
                loader.download_post(post, target=target_path)

                await ctx.send("貼文影像讀取完成！")

            async with ctx.typing():
                filenames = os.listdir(target_path)

                for filename in filenames:
                    file_extension = os.path.splitext(filename)[1].lower()
                    if file_extension in ALLOWED_EXTENSIONS:
                        filename = f'{target_path}\\{filename}'
                        with open(filename, "rb") as fh:
                            f = discord.File(fh, filename=filename)
                            await ctx.send(file=f)
                
                if video_url:
                    await ctx.send(video_url)
                await ctx.send(caption)
        
        except Exception as exception:
            await ctx.send(f"無法讀取貼文影像。錯誤訊息：`{exception}`")

        self.delete_files(target_path)

    def delete_files(self, folder_path):
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                        os.remove(file_path)

            os.rmdir(folder_path)
        except:
            pass

async def setup(bot):
    await bot.add_cog(Crawler(bot))