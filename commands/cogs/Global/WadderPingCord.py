import nextcord
from nextcord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup

# ! not ready for production


class YTNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channel.start()

    def cog_unload(self):
        self.update_channel.cancel()

    @nextcord.slash_command()
    async def set_channel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        # Set the channel to send updates to
        self.target_channel = channel
        await interaction.send(f'Updates will be sent to {channel.mention}')
        
    @nextcord.slash_command()
    async def set_yt_username(self, interaction: nextcord.Interaction, yt_username: str):
        self.yt_profile_link = f'https://www.youtube.com/user/{yt_username}'
        await interaction.send(f'YouTube profile link set to {self.yt_profile_link}')

    @tasks.loop(seconds=55)  # Adjust the interval as needed
    async def update_channel(self):
        if not hasattr(self, 'yt_profile_link') or not hasattr(self, 'target_channel'):
            return
        
        # Scrape the YouTube channel page
        html_content = requests.get(self.yt_profile_link).text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the latest video or live stream
        video_container = soup.find('div', {'id': 'contents'})
        videos = video_container.find_all('ytd-grid-video-renderer') if video_container else []

        # Get the latest video
        latest_video = videos[0] if videos else None
        if latest_video:
            video = latest_video.find('a', id='video-title')
        else:
            video = None

        if video is None:
            return

        # Check if it's a new video
        latest_video_link = 'https://www.youtube.com' + video['href']
        latest_video_title = video['title']

        if not hasattr(self, 'previous_video_link') or self.previous_video_link != latest_video_link:
            self.previous_video_link = latest_video_link
            await self.target_channel.send(f'**New video:** {latest_video_title}\n{latest_video_link}')

def setup(bot):
    bot.add_cog(YTNotifier(bot))
