import json
import nextcord
from nextcord.ext import commands
import os
from nextcord.ui import Button
import requests

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(name="dev")
    async def dev(self, interaction: nextcord.Interaction):
        pass

    @dev.subcommand(name="developer", description="Get developer info")
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
    
    @dev.subcommand(name="commands2", description="Get list of available commands")
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


    @dev.subcommand(name="rolemembers", description="List members in a specific role")
    async def rolemembers(self, interaction: nextcord.Interaction, role: nextcord.Role):
        try:
            members = role.members

            if members:
                member_list = "\n".join([member.name for member in members])
                embed = nextcord.Embed(title=f"Members in {role.name}", color=nextcord.Color.teal())
                embed.description = member_list
            else:
                embed = nextcord.Embed(title=f"No members in {role.name}", color=nextcord.Color.red())

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(color=nextcord.Color.red())
            error_embed.title = "Error Occurred"
            error_embed.description = "An error occurred while executing the command."
            await interaction.send(embed=error_embed)
            
    @dev.subcommand(name="temperature1", description="Convert temperature between Celsius and Fahrenheit")
    async def temperature1(self, interaction: nextcord.Interaction, value: float, unit: str):
        try:
            celsius = None
            fahrenheit = None

            if unit.lower() == "c":
                celsius = value
                fahrenheit = (value * 9/5) + 32
            elif unit.lower() == "f":
                fahrenheit = value
                celsius = (value - 32) * 5/9

            embed = nextcord.Embed(title="Temperature Conversion", color=nextcord.Color.dark_teal())
            embed.add_field(name="Celsius", value=f"{celsius}°C", inline=True)
            embed.add_field(name="Fahrenheit", value=f"{fahrenheit}°F", inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(color=nextcord.Color.red())
            error_embed.title = "Error Occurred"
            error_embed.description = "An error occurred while executing the command."
            await interaction.send(embed=error_embed)
            
    @dev.subcommand(name="factorial", description="Calculate the factorial of a number")
    async def factorial(self, interaction: nextcord.Interaction, number: int):
        try:
            result = 1
            for i in range(1, number + 1):
                result *= i

            embed = nextcord.Embed(title="Factorial Calculation", color=nextcord.Color.blurple())
            embed.add_field(name="Number", value=number, inline=True)
            embed.add_field(name="Factorial", value=result, inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(color=nextcord.Color.red())
            error_embed.title = "Error Occurred"
            error_embed.description = "An error occurred while executing the command."
            await interaction.send(embed=error_embed)
            
    @dev.subcommand(name="serverchannels", description="Get information about server channels")
    async def serverchannels(self, interaction: nextcord.Interaction):
        try:
            guild = interaction.guild

            embed = nextcord.Embed(title="Server Channels", color=nextcord.Color.purple())

            for category in guild.categories:
                category_channels = [channel.name for channel in category.channels if isinstance(channel, nextcord.TextChannel)]
                if category_channels:
                    embed.add_field(name=category.name, value="\n".join(category_channels), inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while executing the command.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
    @dev.subcommand(name="serverinfo2", description="Get information about the server")
    async def serverinfo2(self, interaction: nextcord.Interaction):
        try:
            guild = interaction.guild

            # Member Statistics
            member_count = guild.member_count
            online_count = len([member for member in guild.members if member.status != nextcord.Status.offline])
            bot_count = len([member for member in guild.members if member.bot])

            # Channel Counts
            text_channel_count = len(guild.text_channels)
            voice_channel_count = len(guild.voice_channels)
            category_count = len(guild.categories)

            # Server Features
            features = ", ".join(guild.features) if guild.features else "None"

            # Create Embed
            embed = nextcord.Embed(title="Server Information", color=nextcord.Color.green())
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="Name", value=guild.name, inline=True)
            embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
            embed.add_field(name="Members", value=f"Total: {member_count}\nOnline: {online_count}\nBots: {bot_count}", inline=False)
            embed.add_field(name="Channels", value=f"Text Channels: {text_channel_count}\nVoice Channels: {voice_channel_count}\nCategories: {category_count}", inline=False)
            embed.add_field(name="Features", value=features, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while executing the command.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev.subcommand(name="serverdetails", description="Get detailed information about the server")
    async def serverdetails(self, interaction: nextcord.Interaction):
        try:
            guild = interaction.guild

            # Role Hierarchy
            roles = guild.roles[1:]  # Exclude @everyone role
            sorted_roles = sorted(roles, key=lambda r: r.position, reverse=True)
            role_hierarchy = "\n".join([f"{role.name}: {role.position}" for role in sorted_roles])

            # Member Presence
            online_members = []
            idle_members = []
            offline_members = []

            for member in guild.members:
                if member.status == nextcord.Status.online:
                    online_members.append(member.display_name)
                elif member.status == nextcord.Status.idle:
                    idle_members.append(member.display_name)
                else:
                    offline_members.append(member.display_name)

            # Create Embed
            embed = nextcord.Embed(title="Server Details", color=nextcord.Color.blurple())
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="Member Count", value=f"Total: {guild.member_count}\nOnline: {len(online_members)}\nIdle: {len(idle_members)}\nOffline: {len(offline_members)}", inline=False)
            embed.add_field(name="Role Hierarchy", value=role_hierarchy, inline=False)
            embed.add_field(name="Online Members", value=", ".join(online_members) if online_members else "None", inline=False)
            embed.add_field(name="Idle Members", value=", ".join(idle_members) if idle_members else "None", inline=False)
            embed.add_field(name="Offline Members", value=", ".join(offline_members) if offline_members else "None", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while executing the command.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


    @dev.subcommand(name="catfact", description="Get a random cat fact")
    async def catfact(self, interaction: nextcord.Interaction):
        try:
            # Fetch data from the API
            response = requests.get("https://cat-fact.herokuapp.com/facts/random")
            data = response.json()

            # Extract the cat fact
            cat_fact = data["text"]

            # Create Embed
            embed = nextcord.Embed(title="Random Cat Fact", description=cat_fact, color=nextcord.Color.orange())

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while executing the command.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev.subcommand(name="countryinfo", description="Get information about a country")
    async def countryinfo(self, interaction: nextcord.Interaction, country: str):
        try:
            # Fetch country data from the API
            response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
            data = response.json()

            # Extract relevant country information
            country_data = data[0]
            country_name = country_data["name"]["official"]
            country_capital = country_data["capital"][0]
            country_population = country_data["population"]
            country_area = country_data["area"]

            # Create Embed
            embed = nextcord.Embed(title="Country Information", color=nextcord.Color.gold())
            embed.add_field(name="Country", value=country_name, inline=True)
            embed.add_field(name="Capital", value=country_capital, inline=True)
            embed.add_field(name="Population", value=country_population, inline=True)
            embed.add_field(name="Area", value=country_area, inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while executing the command.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev.subcommand(name="exchangerates", description="Get the latest exchange rates")
    async def exchangerates(self, interaction: nextcord.Interaction):
        try:
            response = requests.get("https://api.exchangerate.host/latest")
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()
            if "rates" in data:
                base_currency = data["base"]
                rates = data["rates"]

                # Create Embed
                embed = nextcord.Embed(title="💱 Latest Exchange Rates", color=nextcord.Color.blue())
                embed.set_thumbnail(url="https://example.com/exchangerate_icon.png")
                embed.add_field(name="Base Currency", value=f"`{base_currency}`", inline=True)

                # Add rate fields
                for currency, rate in rates.items():
                    embed.add_field(name=currency, value=f"```\n{rate:,.2f}\n```", inline=True)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise ValueError("Invalid response format")

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching exchange rates.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev.subcommand(name="dexsearch", description="Search DEX data")
    async def dexsearch(self, interaction: nextcord.Interaction, query: str):
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Extract relevant information
            if "results" in data:
                results = data["results"]

                # Create Embed
                embed = nextcord.Embed(title="DEX Search Results", color=nextcord.Color.blue())

                for result in results:
                    name = result["name"]
                    symbol = result["symbol"]
                    volume = result["volume"]

                    embed.add_field(name=name, value=f"Symbol: {symbol}\nVolume: {volume}", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise ValueError("Invalid response format")

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching DEX data.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Developer(bot))





