import json
import os
import nextcord
from nextcord.ext import commands

class PartnerShip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.global_channels = self.load_global_channels()

    def load_global_channels(self):
        try:
            file_path = os.path.join("data", "global_channels.json")
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_global_channels(self):
        file_path = os.path.join("data", "global_channels.json")
        with open(file_path, "w") as f:
            json.dump(self.global_channels, f)

    def add_global_channel(self, guild, channel):
        self.global_channels[str(guild.id)] = channel.id
        self.save_global_channels()

    def get_global_channel(self, guild):
        channel_id = self.global_channels.get(str(guild.id))
        return guild.get_channel(channel_id) if channel_id else None

    @commands.has_permissions(administrator=True)
    @nextcord.slash_command(name="setupglobalchannel")
    async def setup_global_channel(self, interaction: nextcord.Interaction):
        existing_channel = self.get_global_channel(interaction.guild)
        if existing_channel:
            await interaction.send(f"Global channel already exists: {existing_channel.mention}")
        else:
            new_channel_name = "🌎 global-buzz"
            new_channel = await interaction.guild.create_text_channel(new_channel_name)
            self.add_global_channel(interaction.guild, new_channel)
            await interaction.send(f"Global channel created: {new_channel.mention}")

    @nextcord.slash_command(name="shareevent", description="Share event details to the global channel")
    async def share_event(self, interaction: nextcord.Interaction, event_name: str, event_description: str, event_url: str, scheduled_start_time: str):
        embed = nextcord.Embed(title=f"{event_name} 🎉", description=event_description, url=event_url, color=nextcord.Color.blue())
        embed.add_field(name="Scheduled Start Time ⏰", value=scheduled_start_time, inline=False)
        embed.add_field(name="Event URL 🔗", value=f"[Click here to join the event]({event_url})", inline=False)
        embed.set_footer(text="Shared by: " + str(interaction.user))

        shared = False
        for guild_id, channel_id in self.global_channels.items():
            guild = self.bot.get_guild(int(guild_id))
            if guild:
                channel = guild.get_channel(channel_id)
                if channel:
                    await channel.send("📢 **New Event Announcement!** 📢")
                    await channel.send(embed=embed)
                    await channel.send(f"Event URL: {event_url}")  # Send the event URL as a separate message
                    shared = True

        if shared:
            await interaction.send("Event shared to the global channels!")
        else:
            await interaction.send("No global channels found. Please set up a global channel using /setupglobalchannel.")

def setup(bot):
    bot.add_cog(PartnerShip(bot))



