import nextcord
from nextcord.ext import commands
import json
from pymongo import MongoClient
import urllib.parse

# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]
welcome_settings_collection = db["welcome_settings"]

# ** Ready for Production **

class WelcomeMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_settings_collection = welcome_settings_collection
        self.settings = self.load_settings()

    def load_settings(self):
        result = self.welcome_settings_collection.find_one()
        return result if result else {}

    def save_settings(self):
        self.welcome_settings_collection.replace_one({}, self.settings, upsert=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        welcome_channel_id = self.settings.get(str(guild.id), {}).get("welcome_channel_id")
        welcome_message = self.settings.get(str(guild.id), {}).get("welcome_message")
        welcome_enabled = self.settings.get(str(guild.id), {}).get("welcome_enabled", True)

        if welcome_enabled and welcome_channel_id:
            channel = guild.get_channel(welcome_channel_id)
            if channel:
                embed = nextcord.Embed(
                    title=f"Welcome to {guild.name}!",
                    description=f"{member.mention} has joined the server.",
                    color=0x3498DB
                )
                embed.set_thumbnail(url=member.avatar.url)
                embed.add_field(name="Member Count", value=f"We now have {guild.member_count} members!")
                embed.set_footer(text=f"User ID: {member.id} • Joined at: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")
                await channel.send(content=f"{member.mention}", embed=embed)

        if welcome_enabled and welcome_message:
            try:
                await member.send(welcome_message)
            except nextcord.errors.Forbidden:
                pass

    @nextcord.slash_command(name="setwelcome", description="Set the welcome channel for the server.")
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        guild_id = str(interaction.guild.id)
        self.settings.setdefault(guild_id, {})
        self.settings[guild_id]["welcome_channel_id"] = channel.id
        self.save_settings()
        await interaction.send(f"Welcome channel set to {channel.mention}.")

    @setwelcomechannel.error
    async def setwelcomechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid text channel.")
        else:
            await ctx.send("An error occurred while processing this command.")

    @nextcord.slash_command(name="togglewelcome", description="Toggle the welcome system.")
    @commands.has_permissions(administrator=True)
    async def togglewelcome(self, interaction: nextcord.Interaction):
        guild_id = str(interaction.guild.id)
        welcome_enabled = self.settings.get(guild_id, {}).get("welcome_enabled", True)
        welcome_enabled = not welcome_enabled
        self.settings.setdefault(guild_id, {})
        self.settings[guild_id]["welcome_enabled"] = welcome_enabled
        self.save_settings()
        enabled_status = "enabled" if welcome_enabled else "disabled"
        await interaction.send(f"The welcome system has been {enabled_status}.")

    @togglewelcome.error
    async def togglewelcome_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        else:
            await ctx.send("An error occurred while processing this command.")


def setup(bot):
    bot.add_cog(WelcomeMessage(bot))
