import nextcord
from nextcord.ext import commands



# Define the cog class
class CustomEmbedMaker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="custom_embed", description="Create a custom embed.")
    @commands.has_permissions(administrator=True)
    async def custom_embed(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel, title: str, description: str, color: int):
        await interaction.response.defer()
        
        # Create the embed
        embed = nextcord.Embed(title=title, description=description, color=color)

        # Send the embed
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(CustomEmbedMaker(bot))



