import nextcord
from nextcord.ext import commands

class EmbedCus(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Embed Maker",
        )
        self.emTitle = nextcord.ui.TextInput(label="Embed Title", min_length=2, max_length=124, required=True, placeholder="Enter the embed title here")
        self.add_item(self.emTitle)
        self.emDesc = nextcord.ui.TextInput(label="Embed Description", min_length=5, max_length=4000, required=True, placeholder="Enter the embed description here", style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.emDesc)
        self.channelID = nextcord.ui.TextInput(label="Channel ID", required=True, placeholder="Enter the channel ID")

    async def callback(self, interaction: nextcord.Interaction) -> None:
        title = self.emTitle.value
        desc = self.emDesc.value
        channel_id = int(self.channelID.value)
        em = nextcord.Embed(title=title, description=desc)
        target_channel = interaction.guild.get_channel(channel_id)
        if target_channel:
            await target_channel.send(embed=em)
            await interaction.response.send_message("Embed sent successfully!")
        else:
            await interaction.response.send_message("Invalid channel ID. Please try again.")

class UserMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="cusembed", description="Create an embed")
    async def embed(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(EmbedCus())

def setup(bot):
    bot.add_cog(UserMod(bot))
