import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View
import json

ACTIVE_BUTTONS_FILE = "active_buttons.json"

class SupportView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.active_channels = {}

    async def create_private_channel(self, user_id):
        guild = self.bot.get_guild(self.bot.guilds[0].id)  # Get the first guild the bot is in
        private_channel = await guild.create_text_channel(f"private-channel-{user_id}")
        self.active_channels[user_id] = private_channel.id
        self.save_active_buttons()

        return private_channel

    def load_active_buttons(self):
        try:
            with open(ACTIVE_BUTTONS_FILE, "r") as file:
                self.active_channels = json.load(file)
        except FileNotFoundError:
            self.active_channels = {}

    def save_active_buttons(self):
        with open(ACTIVE_BUTTONS_FILE, "w") as file:
            json.dump(self.active_channels, file)

    @button(label="Technical Support", style=nextcord.ButtonStyle.green)
    async def technical_support(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        private_channel_id = self.active_channels.get(user_id)
        if not private_channel_id:
            private_channel = await self.create_private_channel(user_id)
        else:
            private_channel = self.bot.get_channel(private_channel_id)

        await private_channel.send(f"{interaction.user.mention} requested technical support.")
        await interaction.response.send_message("Technical support request submitted.", ephemeral=True)

    @button(label="Billing Support", style=nextcord.ButtonStyle.green)
    async def billing_support(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        private_channel_id = self.active_channels.get(user_id)
        if not private_channel_id:
            private_channel = await self.create_private_channel(user_id)
        else:
            private_channel = self.bot.get_channel(private_channel_id)

        await private_channel.send(f"{interaction.user.mention} requested billing support.")
        await interaction.response.send_message("Billing support request submitted.", ephemeral=True)

    @button(label="General Inquiry", style=nextcord.ButtonStyle.green)
    async def general_inquiry(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        private_channel_id = self.active_channels.get(user_id)
        if not private_channel_id:
            private_channel = await self.create_private_channel(user_id)
        else:
            private_channel = self.bot.get_channel(private_channel_id)

        await private_channel.send(f"{interaction.user.mention} has a general inquiry.")
        await interaction.response.send_message("General inquiry submitted.", ephemeral=True)

class SupportSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.support_view = SupportView(self.bot)

    def load_active_buttons(self):
        try:
            with open(ACTIVE_BUTTONS_FILE, "r") as file:
                self.support_view.active_channels = json.load(file)
        except FileNotFoundError:
            self.support_view.active_channels = {}

    def save_active_buttons(self):
        with open(ACTIVE_BUTTONS_FILE, "w") as file:
            json.dump(self.support_view.active_channels, file)

    @nextcord.slash_command(name="setupbil")
    @commands.has_permissions(administrator=True)
    async def setupbil(self, interaction: nextcord.Interaction):
        private_channel = await interaction.guild.create_text_channel("private-channel", overwrites={
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        })

        support_channel = await interaction.guild.create_text_channel("support-channel")
        view = self.support_view
        await support_channel.send("Click a button to request technical support, billing support, or make a general inquiry.", view=view)

def setup(bot):
    bot.add_cog(SupportSystemCog(bot))
