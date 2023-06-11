
# bad ass (add a json file to keep buttonss sactive ) and diff private channels for each

import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

#! not ready for production

class MainView(View):
    def __init__(self, bot, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel_id = channel_id

    @button(label="Ticket", style=nextcord.ButtonStyle.green)
    async def ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} opened a ticket.")
        await interaction.response.send_message("Ticket created.", ephemeral=True)

    @button(label="Staff Application", style=nextcord.ButtonStyle.green)
    async def staff_application(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} submitted a staff application.")
        await interaction.response.send_message("Staff application submitted.", ephemeral=True)

    @button(label="Suggestion", style=nextcord.ButtonStyle.green)
    async def suggestion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} submitted a suggestion.")
        await interaction.response.send_message("Suggestion submitted.", ephemeral=True)

    @button(label="Report Bug", style=nextcord.ButtonStyle.red)
    async def report_bug(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} reported a bug.")
        await interaction.response.send_message("Bug report submitted.", ephemeral=True)
        
    @button(label="Join Event", style=nextcord.ButtonStyle.green)
    async def join_event(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} wants to join an event.")
        await interaction.response.send_message("Request to join event submitted.", ephemeral=True)

    @button(label="Request Help", style=nextcord.ButtonStyle.green)
    async def request_help(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} requested help.")
        await interaction.response.send_message("Help request submitted.", ephemeral=True)
        
        
    @button(label="Share Feedback", style=nextcord.ButtonStyle.green)
    async def share_feedback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} shared feedback.")
        await interaction.response.send_message("Feedback submitted.", ephemeral=True)

    @button(label="Ask Question", style=nextcord.ButtonStyle.green)
    async def ask_question(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} asked a question.")
        await interaction.response.send_message("Question submitted.", ephemeral=True)

    @button(label="Submit Artwork", style=nextcord.ButtonStyle.green)
    async def submit_artwork(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} submitted artwork.")
        await interaction.response.send_message("Artwork submission received.", ephemeral=True)
        
    @button(label="Music Recommendation", style=nextcord.ButtonStyle.green)
    async def music_recommendation(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} recommended music.")
        await interaction.response.send_message("Music recommendation submitted.", ephemeral=True)

    @button(label="Promote Content", style=nextcord.ButtonStyle.green)
    async def promote_content(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} wants to promote content.")
        await interaction.response.send_message("Content promotion request submitted.", ephemeral=True)

    @button(label="Submit Tutorial", style=nextcord.ButtonStyle.green)
    async def submit_tutorial(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} submitted a tutorial.")
        await interaction.response.send_message("Tutorial submission received.", ephemeral=True)

class ServerSetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, interaction: nextcord.Interaction):
        private_channel = await interaction.guild.create_text_channel("private-channel", overwrites={
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        })

        main_channel = await interaction.guild.create_text_channel("main-channel")
        view = MainView(self.bot, private_channel.id)
        await main_channel.send("Click a button to open a ticket, submit a staff application, submit a suggestion, or report a bug.", view=view)

def setup(bot):
    bot.add_cog(ServerSetupCog(bot))