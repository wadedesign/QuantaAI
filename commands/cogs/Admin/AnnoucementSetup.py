import asyncio
import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
announcement_collection = db["announcements"]

class AnnouncementManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_settings()

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @nextcord.slash_command(name="announcement", description="Create and manage automated announcements")
    async def announcement(self, interaction: nextcord.Interaction, subcommand: str, *args):
        pass

    @announcement.subcommand(description="Set announcement channel")
    async def set_channel(self, interaction: nextcord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.settings:
            self.settings[guild_id] = {}
        self.settings[guild_id]["channel_id"] = interaction.channel.id
        self.save_settings()
        await interaction.response.send_message("Announcement channel set to this channel.")

    @announcement.subcommand(description="Schedule an announcement")
    async def schedule(self, interaction: nextcord.Interaction, announcement_type: str, details: str, time_str: str):
        try:
            time_delta = self.parse_time(time_str)
            await interaction.response.send_message(f"Scheduled {announcement_type} announcement for {time_str} from now.")
            await asyncio.sleep(time_delta.total_seconds())
            if announcement_type == "maintenance":
                await self.send_maintenance_announcement(interaction.guild, details)
            elif announcement_type == "feature":
                await self.send_feature_announcement(interaction.guild, details)
            else:
                await interaction.channel.send("Invalid announcement type.")
        except ValueError:
            await interaction.response.send_message("Invalid time format. Use format: `1h30m`")

    def parse_time(self, time_str: str):
        time_str = time_str.lower()
        hours = 0
        minutes = 0

        if 'h' in time_str:
            hours, time_str = time_str.split('h')
            hours = int(hours)
        if 'm' in time_str:
            minutes, _ = time_str.split('m')
            minutes = int(minutes)

        if hours == 0 and minutes == 0:
            raise ValueError("Invalid time format")

        return timedelta(hours=hours, minutes=minutes)

    async def send_maintenance_announcement(self, guild: nextcord.Guild, details: str):
        announcement_channel = self.get_announcement_channel(guild)
        if announcement_channel:
            await announcement_channel.send(f"🔧 Scheduled maintenance: {details}")

    async def send_feature_announcement(self, guild: nextcord.Guild, details: str):
        announcement_channel = self.get_announcement_channel(guild)
        if announcement_channel:
            await announcement_channel.send(f"🚀 New feature: {details}")

    def get_announcement_channel(self, guild: nextcord.Guild):
        guild_id = str(guild.id)
        channel_id = self.settings[guild_id]["channel_id"]
        return guild.get_channel(channel_id)

    def load_settings(self):
        settings = announcement_collection.find_one({}, {"_id": 0})
        if settings:
            self.settings = settings
        else:
            self.settings = {}

    def save_settings(self):
        announcement_collection.replace_one({}, self.settings, upsert=True)

def setup(bot):
    bot.add_cog(AnnouncementManager(bot))


