import random
import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import button, View

# ! not ready yet


class SupportView(View):
    def __init__(self, bot, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel_id = channel_id

    @button(label="Technical Support", style=nextcord.ButtonStyle.green)
    async def technical_support(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} requested technical support.")
        await interaction.response.send_message("Technical support request submitted.", ephemeral=True)

    @button(label="Billing Support", style=nextcord.ButtonStyle.green)
    async def billing_support(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} requested billing support.")
        await interaction.response.send_message("Billing support request submitted.", ephemeral=True)

    @button(label="General Inquiry", style=nextcord.ButtonStyle.green)
    async def general_inquiry(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        private_channel = self.bot.get_channel(self.channel_id)
        await private_channel.send(f"{interaction.user.mention} has a general inquiry.")
        await interaction.response.send_message("General inquiry submitted.", ephemeral=True)

class SupportSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setupbil")
    @commands.has_permissions(administrator=True)
    async def setupbil(self, interaction: nextcord.Interaction):
        private_channel = await interaction.guild.create_text_channel("private-channel", overwrites={
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        })

        support_channel = await interaction.guild.create_text_channel("support-channel")
        view = SupportView(self.bot, private_channel.id)
        await support_channel.send("Click a button to request technical support, billing support, or make a general inquiry.", view=view)

def setup(bot):
    bot.add_cog(SupportSystemCog(bot))
# bad ass (add a json file to keep buttonss sactive )
