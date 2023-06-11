import re
import nextcord
from nextcord.ext import commands

# * Works well lets put it in a embed! 

# !not ready for production


class YouTubeWatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_urls = {}  # To store YouTube URLs set by users

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        youtube_urls = self.extract_youtube_urls(message.content)
        if youtube_urls:
            user_id = message.author.id
            if user_id not in self.user_urls:
                self.user_urls[user_id] = set()

            for url in youtube_urls:
                if url not in self.user_urls[user_id]:
                    self.user_urls[user_id].add(url)
                    await message.channel.send(f'New YouTube video added for {message.author.mention}: {url}')

    def extract_youtube_urls(self, text):
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/((watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11}))'
        urls = re.findall(youtube_regex, text)
        return [f'https://youtu.be/{url[-1]}' for url in urls]

    @commands.command()
    async def my_youtube_urls(self, ctx):
        user_id = ctx.author.id
        if user_id in self.user_urls and self.user_urls[user_id]:
            urls = '\n'.join(self.user_urls[user_id])
            await ctx.send(f'Your YouTube URLs:\n{urls}')
        else:
            await ctx.send(f'You have not added any YouTube URLs.')

def setup(bot):
    bot.add_cog(YouTubeWatcher(bot))
