import nextcord
from nextcord.ext import commands

class EmbedModal(nextcord.ui.Modal):

  def __init__(self):

    super().__init__("Create Embed")

    self.title = nextcord.ui.TextInput(label="Title", min_length=1, max_length=256)
    self.description = nextcord.ui.TextInput(label="Description", style=nextcord.TextInputStyle.paragraph, min_length=1, max_length=2048)

    self.channel = nextcord.ui.TextInput(label="Channel ID", placeholder="Enter channel ID", min_length=1, max_length=1024)
    
    self.author = nextcord.ui.TextInput(label="Author Name", min_length=1, max_length=256)

    self.color = nextcord.ui.Select(
      options=[
        nextcord.SelectOption(label="Red", value=0xFF0000),
        nextcord.SelectOption(label="Green", value=0x00FF00),
        nextcord.SelectOption(label="Blue", value=0x0000FF)
      ],
      placeholder="Select color"
    )

    self.add_item(self.title)
    self.add_item(self.description)
    self.add_item(self.channel)  
    self.add_item(self.author)
    self.add_item(self.color)

  def __dict__(self):
    dict = super().__dict__()
    dict['title'] = self.title.value
    dict['description'] = self.description.value
    dict['channel'] = self.channel.value
    dict['author'] = self.author.value
    dict['color'] = self.color.values[0] if self.color.values else None
    return dict

  async def callback(self, interaction):
    embed = nextcord.Embed(
      title=self.title.value,
      description=self.description.value,
      color=int(self.color.values[0], 16) if self.color.values else None
    )
    
    if self.author.value:
      embed.set_author(name=self.author.value)
    
    channel_id = self.channel.value if self.channel.value else None
    if channel_id:
      channel = interaction.guild.get_channel(int(channel_id))
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

