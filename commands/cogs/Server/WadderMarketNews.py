import nextcord
from nextcord.ext import commands, tasks
import feedparser
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
news_collection = db["news"]

class MarketNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC,^DJI,^IXIC&region=US&lang=en-US'
        self.update_news.start()

    def cog_unload(self):
        self.update_news.cancel()

    @nextcord.slash_command()
    @commands.has_permissions(administrator=True)  # Only admins can set the news channel
    async def snewschannel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        guild_id = interaction.guild.id
        channel_id = channel.id

        news_collection.update_one({"guild_id": guild_id}, {"$set": {"channel_id": channel_id}}, upsert=True)

        await interaction.send(f"Market news channel set to {channel.mention}.")

    @tasks.loop(minutes=60)  # Update the news every 60 minutes
    async def update_news(self):
        news_channels = news_collection.find()
        for news_channel in news_channels:
            guild_id = news_channel["guild_id"]
            channel_id = news_channel["channel_id"]
            guild = self.bot.get_guild(guild_id)
            channel = guild.get_channel(channel_id)

            if channel:
                feed = feedparser.parse(self.feed_url)
                entries = feed.entries
                if entries:
                    embed = nextcord.Embed(title='Latest Market News', color=0x2ecc71)
                    for entry in entries:
                        embed.add_field(name=entry['title'], value=entry['link'], inline=False)
                    await channel.send(embed=embed)

    @update_news.before_loop
    async def before_update_news(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(MarketNews(bot))
