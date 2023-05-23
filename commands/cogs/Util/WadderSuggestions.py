import datetime
import nextcord
from nextcord.ext import commands

#own cog! 
suggestion_channel_name = "💡suggestions"

class Suggestions1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="suggestions", description="Commands for managing suggestions")
    async def suggestionstest(self, interaction: nextcord.Interaction):
        pass

    @suggestionstest.subcommand(name="setup", description="Sets up a suggestion channel")
    @commands.has_permissions(administrator=True)
    async def setup_suggestionstest(self, interaction: nextcord.Interaction):
        suggestion_category_name = "📝 Suggestions"
        suggestion_category = await interaction.guild.create_category(suggestion_category_name)

        overwrites = {
        interaction.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
    }
        suggestion_channel = await interaction.guild.create_text_channel(suggestion_channel_name, category=suggestion_category, overwrites=overwrites)

        await interaction.response.send_message("Suggestion channel has been set up.")


    @suggestionstest.subcommand(name="submit", description="Submit a suggestion")
    async def suggest(self, interaction: nextcord.Interaction, title: str, description: str):
        suggestion_channel = nextcord.utils.get(interaction.guild.text_channels, name=suggestion_channel_name)

        if suggestion_channel is None:
            await interaction.response.send_message("Suggestion channel not found. Please set up a suggestion channel using /suggestions setup first.", ephemeral=True)
            return

        embed = nextcord.Embed(title=f"📢 {title}", description=description, color=nextcord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Suggested by {interaction.user}", icon_url=interaction.user.avatar.url)

        
        # Send the suggestion and add reactions
        suggestion_message = await suggestion_channel.send(embed=embed)
        await suggestion_message.add_reaction("⬆️")
        await suggestion_message.add_reaction("⬇️")

        await interaction.response.send_message("Your suggestion has been received.", ephemeral=True)

def setup(bot):
    bot.add_cog(Suggestions1(bot))