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
        self.add_item(self.channelID)
        self.footerText = nextcord.ui.TextInput(label="Footer Text", min_length=1, max_length=2048, required=False, placeholder="Enter the footer text")
        self.add_item(self.footerText)
        self.timestamp = nextcord.ui.Checkbox(label="Timestamp", required=False)
        self.add_item(self.timestamp)
        self.footerImage = nextcord.ui.TextInput(label="Footer Image URL", required=False, placeholder="Enter the URL of the footer image")
        self.add_item(self.footerImage)
        self.color = nextcord.ui.ColorInput(label="Color", required=False, default=nextcord.Color.blurple())
        self.add_item(self.color)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        title = self.emTitle.value
        desc = self.emDesc.value
        channel_id = int(self.channelID.value) if self.channelID.value is not None else None
        em = nextcord.Embed(title=title, description=desc)
        
        footer_text = self.footerText.value
        if footer_text:
            em.set_footer(text=footer_text)
        
        if self.timestamp.checked:
            em.timestamp = nextcord.utils.utcnow()
        
        footer_image_url = self.footerImage.value
        if footer_image_url:
            em.set_footer(icon_url=footer_image_url)
        
        em.color = self.color.value
        
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
