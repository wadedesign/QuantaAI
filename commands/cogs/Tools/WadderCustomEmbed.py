import nextcord
from nextcord.ext import commands

# Ready for Production 

class EmbedCus(nextcord.ui.Modal):

  def __init__(self):
    super().__init__("Embed Maker")
    
    self.emTitle = nextcord.ui.TextInput(label="Embed Title", min_length=2, max_length=124, required=True, placeholder="Enter the embed title here")
    self.add_item(self.emTitle)
    
    self.emDesc = nextcord.ui.TextInput(label="Embed Description", min_length=5, max_length=2048, required=True, placeholder="Enter the embed description here", style=nextcord.TextInputStyle.paragraph)
    self.add_item(self.emDesc)
    
    self.channelID = nextcord.ui.TextInput(label="Channel ID", required=True, placeholder="Enter the channel ID")
    self.add_item(self.channelID)

    self.color = nextcord.ui.TextInput(label="Color", placeholder="Enter hex color code")
    self.add_item(self.color)
    
    self.footerText = nextcord.ui.TextInput(label="Footer Text", min_length=1, max_length=2048, required=False, placeholder="Enter footer text")
    self.add_item(self.footerText)

    self.footerImage = nextcord.ui.TextInput(label="Footer Image URL", required=False, placeholder="Enter URL of footer image")
    self.add_item(self.footerImage)

    self.authorName = nextcord.ui.TextInput(label="Author Name", min_length=1, max_length=256, required=False, placeholder="Enter author name")
    self.add_item(self.authorName)
    
  async def callback(self, interaction: nextcord.Interaction) -> None:
    title = self.emTitle.value
    desc = self.emDesc.value
    channel_id = int(self.channelID.value) if self.channelID.value else None
    
    em = nextcord.Embed(title=title, description=desc)
    
    color = int(self.color.value, 16) 
    em.color = color
    
    footer_text = self.footerText.value
    footer_image = self.footerImage.value
    author_name = self.authorName.value
    
    if footer_text:
      em.set_footer(text=footer_text)

    if footer_image:
      em.set_footer(icon_url=footer_image)
      
    if author_name:
      em.set_author(name=author_name)

    target_channel = interaction.guild.get_channel(channel_id)
    if target_channel:
      await target_channel.send(embed=em)
      await interaction.response.send_message("Embed sent successfully!")
    else:
      await interaction.response.send_message("Invalid channel ID. Please try again.")
      
# Rest of cog code
      
class UserMod(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(name="cusembed", description="Create an embed")
  async def embed(self, interaction: nextcord.Interaction):
    await interaction.response.send_modal(EmbedCus())
    
def setup(bot):
  bot.add_cog(UserMod(bot))


