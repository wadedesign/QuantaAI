from functools import partial
import nextcord
from nextcord.ext import commands


# works but still errors out. ! delete this file

class ServerHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="serverhelp",description="Shows a list of available commands")
    async def serverhelp(self, interaction:nextcord.Interaction):
        # List of commands to display in the embed
        command_list = [
            ("/add", "Calculate the sum of two numbers"),
            ("/add_role", "Add a role to a user in the server"),
            ("/advertise", "Advertise the bot and its features"),
            ("/advertiseYOU", "Advertise your server in a linked channel"),
            ("/ban", "Ban a user from the server"),
            ("/calculate_average", "Calculate the average of a list of numbers"),
            ("/celsius", "Convert a temperature from Celsius to Fahrenheit"),
            ("/chatbot", "Chat with the OpenAI chatbot"),
            ("/chucknorris", "Get a random Chuck Norris joke"),
            ("/clear", "Deletes a specified number of messages from a channel"),
            ("/codeblock", "Return the input text as a code block"),
            ("/countdown", "Countdown to a specified event"),
        ]

        # Divide the commands into pages of 10 commands each
        pages = [command_list[i:i + 10] for i in range(0, len(command_list), 10)]

        # Create an embed for each page of commands
        embeds = []
        for i, page in enumerate(pages):
            embed = nextcord.Embed(title=f"Page {i + 1}/{len(pages)}", color=0x7289da)
            for command, description in page:
                embed.add_field(name=command, value=description, inline=False)
            embeds.append(embed)

        # Create a view with buttons to navigate between pages
        view = nextcord.ui.View()
        for i in range(len(embeds)):
            button = nextcord.ui.Button(style=nextcord.ButtonStyle.secondary, label=str(i + 1))
            button.callback = partial(self.on_help_button_click, embeds, i, view)
            view.add_item(button)

        # Send the first page of commands with the view
        await interaction.send(embed=embeds[0], view=view)

        async def on_help_button_click(self, embeds, page_index, button, interaction):
            # Check if the message object has a view attribute before accessing it
            if not hasattr(interaction.message, 'view'):
                return
            
            # Update the message with the embed for the clicked page
            message = interaction.message
            await message.edit(embed=embeds[page_index])
            
            # Update the style of the clicked button to indicate that it is selected
            view = message.view  # Access the view from the message
            for item in view.children:
                if isinstance(item, nextcord.ui.Button) and item.label == button.label:
                    item.style = nextcord.ButtonStyle.primary
                else:
                    item.style = nextcord.ButtonStyle.secondary
            
            # Log some information to help debug the issue
            print(f"Page index: {page_index}")
            print(f"Embeds: {len(embeds)}")
            print(f"View children: {len(view.children)}")
            print(f"Button label: {button.label}")
            
            await interaction.edit_original_message(embed=embeds[page_index], view=view)  # Update the embed here


def setup(bot):
    bot.add_cog(ServerHelp(bot))


