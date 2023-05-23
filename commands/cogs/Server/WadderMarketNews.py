import nextcord
from nextcord.ext import commands, tasks
import feedparser

class MarketNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC,^DJI,^IXIC&region=US&lang=en-US'
        self.channel_id = None
        self.update_news.start()

    def cog_unload(self):
        self.update_news.cancel()

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)  # Only admins can set the news channel
    async def snewschannel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        self.channel_id = channel.id
        await interaction.send(f"Market news channel set to {channel.mention}.")

    @tasks.loop(minutes=60)  # Update the news every 60 minutes
    async def update_news(self):
        if self.channel_id:
            feed = feedparser.parse(self.feed_url)
            entries = feed.entries
            if entries:
                embed = nextcord.Embed(title='Latest Market News', color=0x2ecc71)
                for entry in entries:
                    embed.add_field(name=entry['title'], value=entry['link'], inline=False)
                channel = self.bot.get_channel(self.channel_id)
                await channel.send(embed=embed)

    @update_news.before_loop
    async def before_update_news(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(MarketNews(bot))