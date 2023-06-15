import asyncio
import random
import aiohttp
import nextcord
from nextcord.ext import commands
from numbers import Number
from random import randint
from pymongo import MongoClient
import urllib.parse

import requests

BaseCog = getattr(commands, "Cog", object)


# MongoDB connection details
username = urllib.parse.quote_plus("apwade75009")
password = urllib.parse.quote_plus("Celina@12")
cluster = MongoClient(f"mongodb+srv://{username}:{password}@quantaai.irlbjcw.mongodb.net/")
db = cluster["QuantaAI"]  # Replace "YourNewDatabaseName" with your desired database name
nba_collection = db["nba_players"]

## ! Make more sub commands of this! ##


class XKCD(BaseCog):
    """Display XKCD entries"""

    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(name='dev3')
    async def main(self, interaction: nextcord.Interaction):
       pass

    @main.subcommand(name="xkcd", description="To get xkcd comics")
    async def xkcd(self, interaction: nextcord.Interaction, *, entry_number=None):

        # Define the computer animation frames
        animation = [
            "```yaml\n[Fetching xkcd comic...     ]```",
            "```yaml\n[Fetching xkcd comic...•    ]```",
            "```yaml\n[Fetching xkcd comic...••   ]```",
            "```yaml\n[Fetching xkcd comic...•••  ]```",
            "```yaml\n[Fetching xkcd comic...•••• ]```",
            "```yaml\n[Fetching xkcd comic...•••••]```",
            "```yaml\n[Fetching xkcd comic... ••••]```",
            "```yaml\n[Fetching xkcd comic...  •••]```",
            "```yaml\n[Fetching xkcd comic...   ••]```",
            "```yaml\n[Fetching xkcd comic...    •]```",
            "```yaml\n[Fetching xkcd comic...     ]```",
            "```yaml\n[Fetching xkcd comic...    ]```",
            "```yaml\n[Fetching xkcd comic...•   ]```",
            "```yaml\n[Fetching xkcd comic...••  ]```",
            "```yaml\n[Fetching xkcd comic...••• ]```",
            "```yaml\n[Fetching xkcd comic...••••]```",
            "```yaml\n[Fetching xkcd comic...•••••]```",
            "```yaml\n[Fetching xkcd comic...•••• ]```",
            "```yaml\n[Fetching xkcd comic...•••  ]```",
            "```yaml\n[Fetching xkcd comic...••   ]```",
            "```yaml\n[Fetching xkcd comic...•    ]```",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message(animation[0])

        # Animate the loading message
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Fetch the xkcd comic
        headers = {"content-type": "application/json"}
        url_latest = "https://xkcd.com/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url_latest, headers=headers) as response:
                xkcd_latest = await response.json()
                xkcd_max = xkcd_latest.get("num") + 1

        if entry_number is not None and int(entry_number) > 0 and int(entry_number) < xkcd_max:
            i = int(entry_number)
        else:
            i = random.randint(0, xkcd_max)

        url = f"https://xkcd.com/{i}/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd = await response.json()

        # Delete the loading message
        await loading_message.delete()

        # Build Embed
        embed = nextcord.Embed()
        embed.title = f"{xkcd['title']} ({xkcd['day']}/{xkcd['month']}/{xkcd['year']})"
        embed.url = f"https://xkcd.com/{i}"
        embed.description = xkcd["alt"]
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text="Powered by xkcd")
        await interaction.send(embed=embed)


        
    @main.subcommand(name="nba", description="To get NBA players")
    async def nba_player(self, interaction: nextcord.Interaction, name: str):
        search_url = "https://free-nba.p.rapidapi.com/players"
        search_params = {
            "search": name,
            "per_page": 5
        }

        headers = {
            "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
            "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
        }

        search_response = requests.get(search_url, headers=headers, params=search_params)
        search_results = search_response.json()["data"]

        if not search_results:
            await interaction.send("No players found with that name.")
            return

        player_ids = [player["id"] for player in search_results]
        player_data = []

        for player_id in player_ids:
            player_url = f"https://free-nba.p.rapidapi.com/players/{player_id}"
            player_response = requests.get(player_url, headers=headers)
            player_data.append(player_response.json())

        nba_collection.insert_many(player_data)

        for player in player_data:
            player_name = player['first_name'] + " " + player['last_name']
            player_team = player['team']['full_name']
            player_stats = (
                str(player['height_feet'])
                + " ft "
                + str(player['height_inches'])
                + " in, "
                + str(player['weight_pounds'])
                + " lbs"
            )

            image_search_url = "https://api.unsplash.com/search/photos"
            image_search_params = {
                "query": player_name,
                "per_page": 1,
                "client_id": "8_x4s8mZvLnV6ZzBsiEfWIdq8ZL_utvXX5MdtyDgm34"
            }

            image_response = requests.get(image_search_url, params=image_search_params)
            image_data = image_response.json()["results"]

            if image_data:
                player_image = image_data[0]["urls"]["small"]
            else:
                player_image = None

            embed = nextcord.Embed(title="NBA Player Information", description=f"Player: {player_name}", color=0x00ff00)
            embed.add_field(name="Team", value=player_team, inline=False)
            embed.add_field(name="Stats", value=player_stats, inline=False)

            if player_image:
                embed.set_thumbnail(url=player_image)

            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(XKCD(bot))