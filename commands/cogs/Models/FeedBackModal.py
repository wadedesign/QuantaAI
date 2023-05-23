import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

class FeedbackView(View):
    def __init__(self, bot, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel_id = channel_id

    @button(label="Events Feedback", style=nextcord.ButtonStyle.green)
    async def events_feedback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} provided feedback on events.")
        await interaction.response.send_message("Events feedback submitted.", ephemeral=True)

    @button(label="Community Feedback", style=nextcord.ButtonStyle.green)
    async def community_feedback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} provided feedback on the community.")
        await interaction.response.send_message("Community feedback submitted.", ephemeral=True)

    @button(label="Server Management Feedback", style=nextcord.ButtonStyle.green)
    async def server_management_feedback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} provided feedback on server management.")
        await interaction.response.send_message("Server management feedback submitted.", ephemeral=True)

class FeedbackSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setup3")
    @commands.has_permissions(administrator=True)
    async def setup3(self, interaction: nextcord.Interaction):
        private_channel = await interaction.guild.create_text_channel("private-channel", overwrites={
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        })

        feedback_channel = await interaction.guild.create_text_channel("feedback-channel")
        view = FeedbackView(self.bot, private_channel.id)
        await feedback_channel.send("Click a button to provide feedback on events, community, or server management.", view=view)

def setup(bot):
    bot.add_cog(FeedbackSystemCog(bot))
# bad ass (add a json file to keep buttonss sactive )
