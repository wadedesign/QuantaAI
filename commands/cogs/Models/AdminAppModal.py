import json
import nextcord
from nextcord.ext import commands

class AdminApplicationModal(nextcord.ui.Modal):
    def __init__(self, application_channel):
        super().__init__("Admin Application")
        self.application_channel = application_channel

        self.application = nextcord.ui.TextInput(
            label="Application",
            min_length=5,
            max_length=4000,
            required=True,
            placeholder="Enter your application here",
            style=nextcord.TextInputStyle.paragraph,
        )
        self.add_item(self.application)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        application_text = self.application.value
        await self.application_channel.send(f"New admin application from {interaction.user.mention}:\n\n{application_text}")
        await interaction.response.send_message("Your admin application has been submitted!")

class AdminApplications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.application_channels = self.load_application_channels()

    def load_application_channels(self):
        try:
            with open("data/application_channels.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_application_channels(self):
        with open("data/application_channels.json", "w") as f:
            json.dump(self.application_channels, f)

    def add_application_channel(self, guild, channel):
        self.application_channels[str(guild.id)] = channel.id
        self.save_application_channels()

    def get_application_channel(self, guild):
        channel_id = self.application_channels.get(str(guild.id))
        return guild.get_channel(channel_id) if channel_id else None

    @commands.has_permissions(administrator=True)
    @nextcord.slash_command(name="setupapplicationchannel", description="Set up an admin application channel")
    async def setup_application_channel(self, interaction: nextcord.Interaction):
        existing_channel = self.get_application_channel(interaction.guild)
        if existing_channel:
            await interaction.send(f"Application channel already exists: {existing_channel.mention}")
        else:
            new_channel = await interaction.guild.create_text_channel("admin-applications")
            self.add_application_channel(interaction.guild, new_channel)
            await interaction.send(f"Application channel created: {new_channel.mention}")

    @nextcord.slash_command(name="applyforadmin", description="Submit an admin application")
    async def apply_for_admin(self, interaction: nextcord.Interaction):
        application_channel = self.get_application_channel(interaction.guild)
        if application_channel:
            await interaction.response.send_modal(AdminApplicationModal(application_channel))
        else:
            await interaction.send("No application channel found. Please ask an administrator to set up an application channel using /setupapplicationchannel.")

def setup(bot):
    bot.add_cog(AdminApplications(bot))
