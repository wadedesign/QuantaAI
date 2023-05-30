import json
import nextcord
from nextcord.ext import commands
import os
from nextcord.ui import Button

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="developer", description="Get developer info")
    async def developer(self, interaction: nextcord.Interaction):
        config_path = os.path.join(os.getcwd(), "botconfig", "config.json")
        with open(config_path, "r") as config_file:
            config_data = json.load(config_file)

        try:
            embed = nextcord.Embed(color=nextcord.Color.blue())  # Replace with the desired color
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/442355791412854784/df7b527a701d9a1ab6d73213576fe295.webp?size=1024")
            embed.set_author(name="Developer Info", url="https://milrato.eu")
            embed.add_field(name="🆕 NEW GITHUB", value=f"> There is now an **open Source** Version of this Bot on [Tomato#6966's Github](https://github.com/wadder12)\n> [Link](https://github.com/wadder12/QuantaAI) but please make sure to **give __Credits__** if you use it!\n> Make sure to read the [README](https://github.com/wadder12/QuantaAI) and the [WIKI / FAQ](https://github.com/wadder12/QuantaAI) carefully before opening an [ISSUE](https://github.com/wadder12/QuantaAI)")
            
            button = Button(label="Support Server", url="https://discord.com/gg/milrato")
            view = nextcord.ui.View()
            view.add_item(button)

            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(color=nextcord.Color.red())  # Replace with the desired error color
            error_embed.title = "Error Occurred"
            error_embed.description = "An error occurred while executing the command."
            await interaction.send(embed=error_embed)
    @nextcord.slash_command(name="commands2", description="Get list of available commands")
    async def commands2(self, interaction: nextcord.Interaction):
        try:
            command_list = []
            for command in self.bot.commands:
                if not command.hidden:
                    command_list.append(f"`/{command.name}` - {command.description}")

            embed = nextcord.Embed(title="Available Commands", color=nextcord.Color.green())
            embed.description = "\n".join(command_list)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(color=nextcord.Color.red())
            error_embed.title = "Error Occurred"
            error_embed.description = "An error occurred while executing the command."
            await interaction.send(embed=error_embed)

def setup(bot):
    bot.add_cog(Developer(bot))





