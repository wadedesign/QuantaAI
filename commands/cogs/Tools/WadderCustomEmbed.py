import nextcord
from nextcord.ext import commands 

class EmbedModal(nextcord.ui.Modal):

  def __init__(self):

    super().__init__("Create Embed") 
    
    self.title = nextcord.ui.TextInput(label="Title", min_length=1, max_length=256)
    self.description = nextcord.ui.TextInput(label="Description", style=nextcord.TextInputStyle.paragraph)

    self.channel = nextcord.ui.TextInput(label="Channel ID", placeholder="Enter channel ID")

    self.footer = nextcord.ui.TextInput(label="Footer Text", required=False)
    self.footer_image = nextcord.ui.TextInput(label="Footer Image URL", required=False)
    self.author = nextcord.ui.TextInput(label="Author Name", required=False)

    self.color = nextcord.ui.Select(
      options=[
        nextcord.SelectOption(label="Red", value=0xFF0000),
        nextcord.SelectOption(label="Green", value=0x00FF00),
        nextcord.SelectOption(label="Blue", value=0x0000FF)
      ],
      placeholder="Select color"  
    )

    self.add_items(self.title, self.description, self.channel, self.footer, self.footer_image, self.author, self.color)

  async def callback(self, interaction):
    # Get values
    title = self.title.value
    description = self.description.value
    channel = self.channel.value
    
    footer = self.footer.value
    footer_image = self.footer_image.value
    author = self.author.value
    color = int(self.color.values[0]) if self.color.values else None
    
    # Create embed
    embed = nextcord.Embed(title=title, description=description, color=color)
    
    if footer:
      embed.set_footer(text=footer, icon_url=footer_image)  
    if author:
      embed.set_author(name=author)
    
    # Send embed 
    channel_id = int(channel) if channel else None
    if channel_id:
      channel = interaction.guild.get_channel(channel_id)
      await channel.send(embed=embed)
      await interaction.response.send_message("Embed sent!")
    else:
      await interaction.response.send_message("Invalid channel ID")
      
class EmbedCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(name="cusembed", description="Create and send embed")
  async def embed(self, interaction):
    await interaction.response.send_modal(EmbedModal())  

def setup(bot):
  bot.add_cog(EmbedCog(bot))

