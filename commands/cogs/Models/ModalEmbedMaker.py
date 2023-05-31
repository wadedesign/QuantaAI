import nextcord
from nextcord.ext import commands

class EmbedModal(nextcord.ui.Modal): # make send to a channel option
    def __init__(self):
        super().__init__(
            "Embed Maker",
        )
        self.emTitle = nextcord.ui.TextInput(label="Embed Title", min_length=2, max_length=124, required=True, placeholder="Enter the embed title here")
        self.add_item(self.emTitle)
        self.emDesc = nextcord.ui.TextInput(label="Embed Description", min_length=5, max_length=4000, required=True, placeholder="Enter the embed description here", style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.emDesc)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        title = self.emTitle.value
        desc = self.emDesc.value
        em = nextcord.Embed(title=title, description=desc)
        await interaction.response.send_message(embed=em)

class Modals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @nextcord.slash_command(name="embed", description="Create an embed")
    async def embed(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(EmbedModal())

def setup(bot):
    bot.add_cog(Modals(bot))